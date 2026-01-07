import motor.motor_asyncio
import base64
import logging
from datetime import datetime, date
from typing import List, Optional, Dict
from config import * 

logging.basicConfig(level=logging.INFO)


class Master:
    def __init__(self, DB_URL, DB_NAME):
        self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
        self.database = self.dbclient[DB_NAME]

        # Initialize all collections - COMPLETELY SEPARATE
        self.user_data = self.database['users']
        self.channel_data = self.database['channels']  # For link generation ONLY
        self.admins_data = self.database['admins']
        self.del_timer_data = self.database['del_timer']
        self.ban_data = self.database['ban_data']
        self.fsub_data = self.database['fsub']  # For force subscription ONLY
        self.rqst_fsub_data = self.database['request_forcesub']
        self.rqst_fsub_Channel_data = self.database['request_forcesub_channel']

        # Main collection reference (for backward compatibility)
        self.col = self.user_data

    def new_user(self, id, username=None):
        return dict(
            _id=int(id),
            username=username.lower() if username else None,
            join_date=date.today().isoformat(),
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=date.max.isoformat(),
                ban_reason='',
            )
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id, u.username)
            try:
                await self.user_data.insert_one(user)
                logging.info(f"New user added: {u.id}")
            except Exception as e:
                logging.error(f"Error adding user {u.id}: {e}")
        else:
            logging.info(f"User {u.id} already exists")

    async def is_user_exist(self, id):
        try:
            user = await self.user_data.find_one({"_id": int(id)})
            return bool(user)
        except Exception as e:
            logging.error(f"Error checking if user {id} exists: {e}")
            return False

    async def get_all_users(self):
        try:
            all_users = self.user_data.find({})
            return all_users
        except Exception as e:
            logging.error(f"Error getting all users: {e}")
            return None

    async def total_users_count(self):
        try:
            count = await self.user_data.count_documents({})
            return count
        except Exception as e:
            logging.error(f"Error counting users: {e}")
            return 0

    async def delete_user(self, user_id):
        try:
            await self.user_data.delete_many({"_id": int(user_id)})
        except Exception as e:
            logging.error(f"Error deleting user {user_id}: {e}")

    async def is_user_banned(self, user_id):
        try:
            user = await self.ban_data.find_one({"_id": user_id})
            if user and user.get("ban_status", {}).get("is_banned", False):
                return user
        except Exception as e:
            logging.error(f"Error in checking ban status {user_id}: {e}")

    async def is_admin(self, user_id: int) -> bool:
        """Check if a user is an admin."""
        try:
            _id = int(user_id)
            return bool(await self.admins_data.find_one({"_id": user_id}))
        except Exception as e:
            logging.error(f"Error checking admin status for {user_id}: {e}")
            return False

    async def add_admin(self, user_id: int) -> bool:
        """Add a user as admin."""
        try:
            _id = int(user_id)
            await self.admins_data.update_one(
                {"_id": user_id},
                {"$set": {"_id": user_id, "added_at": datetime.utcnow()}},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"Error adding admin {user_id}: {e}")
            return False

    async def remove_admin(self, user_id: int) -> bool:
        """Remove a user from admins."""
        try:
            result = await self.admins_data.delete_one({"_id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            logging.error(f"Error removing admin {user_id}: {e}")
            return False

    async def list_admins(self) -> list:
        """List all admin user IDs."""
        try:
            admins = await self.admins_data.find({}).to_list(None)
            return [admin["_id"] for admin in admins]
        except Exception as e:
            logging.error(f"Error listing admins: {e}")
            return []
            
    # ==================== CHANNEL DATA METHODS (Link Generation Only) ====================
    # These methods ONLY work with 'channels' collection for link generation
    # They DO NOT touch 'fsub' collection
    
    async def save_channel(self, channel_id: int) -> bool:
        """
        Save channel to 'channels' collection for link generation ONLY.
        ⚠️ This does NOT add channel to FSub list.
        ⚠️ Use add_fsub_channel() separately if FSub is needed.
        
        Args:
            channel_id: The channel ID to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        if not isinstance(channel_id, int):
            logging.error(f"[SAVE_CHANNEL] Invalid channel_id: {channel_id}")
            return False

        try:
            # Generate encoded links
            string_bytes = str(channel_id).encode("ascii")
            base64_bytes = base64.urlsafe_b64encode(string_bytes)
            encoded_link = (base64_bytes.decode("ascii")).strip("=")
            req_encoded_link = encoded_link
            
            # Save to 'channels' collection ONLY
            await self.channel_data.update_one(
                {"channel_id": channel_id},
                {
                    "$set": {
                        "channel_id": channel_id,
                        "encoded_link": encoded_link,
                        "req_encoded_link": req_encoded_link,
                        "invite_link_expiry": None,
                        "created_at": datetime.utcnow(),
                        "status": "active"
                    }
                },
                upsert=True
            )
            logging.info(f"✅ [SAVE_CHANNEL] Channel {channel_id} saved to 'channels' collection (link generation)")
            logging.info(f"ℹ️  [SAVE_CHANNEL] Channel {channel_id} is NOT in FSub list (use add_fsub_channel to add)")
            return True
        except Exception as e:
            logging.error(f"❌ [SAVE_CHANNEL] Error saving channel {channel_id}: {e}")
            return False

    async def delete_channel(self, channel_id: int) -> bool:
        """
        Delete channel from 'channels' collection (link generation).
        ⚠️ This does NOT remove channel from FSub list.
        ⚠️ Use remove_fsub_channel() separately to remove from FSub.
        
        Args:
            channel_id: The channel ID to delete
            
        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            result = await self.channel_data.delete_one({"channel_id": channel_id})
            if result.deleted_count > 0:
                logging.info(f"✅ [DELETE_CHANNEL] Channel {channel_id} deleted from 'channels' collection")
                logging.info(f"ℹ️  [DELETE_CHANNEL] Channel {channel_id} may still be in FSub list")
                return True
            else:
                logging.warning(f"⚠️  [DELETE_CHANNEL] Channel {channel_id} not found in 'channels' collection")
                return False
        except Exception as e:
            logging.error(f"❌ [DELETE_CHANNEL] Error deleting channel {channel_id}: {e}")
            return False

    async def get_channels(self) -> List[int]:
        """Get all channel IDs from 'channels' collection (for link generation)."""
        try:
            channels = await self.channel_data.find({"status": "active"}).to_list(None)
            valid_channels = [ch["channel_id"] for ch in channels if "channel_id" in ch]
            logging.info(f"[GET_CHANNELS] Found {len(valid_channels)} channels in 'channels' collection")
            return valid_channels
        except Exception as e:
            logging.error(f"Error fetching channels: {e}")
            return []

    async def show_channels(self) -> List[int]:
        """Alias for get_channels."""
        return await self.get_channels()

    async def get_encoded_link(self, channel_id: int) -> Optional[str]:
        """Get encoded link from 'channels' collection."""
        if not isinstance(channel_id, int):
            logging.error(f"Invalid channel_id: {channel_id}")
            return None

        try:
            channel = await self.channel_data.find_one({"channel_id": channel_id, "status": "active"})
            if channel and "encoded_link" in channel:
                return channel["encoded_link"]
            else:
                logging.warning(f"No encoded_link found for channel {channel_id}")
                return None
        except Exception as e:
            logging.error(f"Error getting encoded link for channel {channel_id}: {e}")
            return None

    async def get_encoded_link2(self, channel_id: int) -> Optional[str]:
        """Get secondary encoded link from 'channels' collection."""
        if not isinstance(channel_id, int):
            logging.error(f"Invalid channel_id: {channel_id}")
            return None

        try:
            channel = await self.channel_data.find_one({"channel_id": channel_id, "status": "active"})
            if channel and "req_encoded_link" in channel:
                return channel["req_encoded_link"]
            else:
                logging.warning(f"No req_encoded_link found for channel {channel_id}")
                return None
        except Exception as e:
            logging.error(f"Error getting secondary encoded link for channel {channel_id}: {e}")
            return None

    async def save_encoded_link(self, channel_id: int) -> Optional[str]:
        """Save encoded link in 'channels' collection."""
        if not isinstance(channel_id, int):
            logging.error(f"Invalid channel_id: {channel_id}")
            return None

        try:
            string_bytes = str(channel_id).encode("ascii")
            base64_bytes = base64.urlsafe_b64encode(string_bytes)
            encoded_link = (base64_bytes.decode("ascii")).strip("=")
            
            await self.channel_data.update_one(
                {"channel_id": channel_id},
                {
                    "$set": {
                        "channel_id": channel_id,
                        "encoded_link": encoded_link,
                        "status": "active",
                        "updated_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
            logging.info(f"Saved encoded link for channel {channel_id}: {encoded_link}")
            return encoded_link
        except Exception as e:
            logging.error(f"Error saving encoded link for channel {channel_id}: {e}")
            return None

    async def get_channel_by_encoded_link(self, encoded_link: str) -> Optional[int]:
        """Get channel ID by encoded link from 'channels' collection."""
        if not isinstance(encoded_link, str):
            logging.error("get_channel_by_encoded_link: encoded_link is not a string")
            return None

        try:
            # First try: Search by encoded_link field
            channel = await self.channel_data.find_one({"encoded_link": encoded_link, "status": "active"})
            
            if channel and "channel_id" in channel:
                return channel["channel_id"]
            
            # Second try: Decode the base64 string
            try:
                base64_string = encoded_link.strip("=")
                base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
                string_bytes = base64.urlsafe_b64decode(base64_bytes)
                decoded_string = string_bytes.decode("ascii")
                decoded_id = int(decoded_string)
                
                # Check if channel exists
                channel = await self.channel_data.find_one({"channel_id": decoded_id})
                
                if channel:
                    # Update the encoded_link field
                    await self.channel_data.update_one(
                        {"channel_id": decoded_id},
                        {
                            "$set": {
                                "encoded_link": encoded_link,
                                "status": "active",
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )
                    return decoded_id
                else:
                    # Create the channel entry
                    string_bytes = str(decoded_id).encode("ascii")
                    base64_bytes = base64.urlsafe_b64encode(string_bytes)
                    new_encoded_link = (base64_bytes.decode("ascii")).strip("=")
                    
                    await self.channel_data.update_one(
                        {"channel_id": decoded_id},
                        {
                            "$set": {
                                "channel_id": decoded_id,
                                "encoded_link": new_encoded_link,
                                "req_encoded_link": new_encoded_link,
                                "status": "active",
                                "created_at": datetime.utcnow()
                            }
                        },
                        upsert=True
                    )
                    return decoded_id
                    
            except Exception as decode_error:
                logging.error(f"Failed to decode base64 '{encoded_link}': {decode_error}")
            
            return None
            
        except Exception as e:
            logging.error(f"Error fetching channel by encoded link {encoded_link}: {e}")
            return None

    async def save_encoded_link2(self, channel_id: int, encoded_link: str) -> Optional[str]:
        """Save secondary encoded link in 'channels' collection."""
        if not isinstance(channel_id, int) or not isinstance(encoded_link, str):
            logging.error(f"Invalid input: channel_id={channel_id}, encoded_link={encoded_link}")
            return None

        try:
            await self.channel_data.update_one(
                {"channel_id": channel_id},
                {
                    "$set": {
                        "channel_id": channel_id,
                        "req_encoded_link": encoded_link,
                        "status": "active",
                        "updated_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
            logging.info(f"Saved req_encoded link for channel {channel_id}: {encoded_link}")
            return encoded_link
        except Exception as e:
            logging.error(f"Error saving secondary encoded link for channel {channel_id}: {e}")
            return None

    async def get_channel_by_encoded_link2(self, encoded_link: str) -> Optional[int]:
        """Get channel ID by secondary encoded link from 'channels' collection."""
        if not isinstance(encoded_link, str):
            logging.error("get_channel_by_encoded_link2: encoded_link is not a string")
            return None

        try:
            # First try: Search by req_encoded_link field
            channel = await self.channel_data.find_one({"req_encoded_link": encoded_link, "status": "active"})
            
            if channel and "channel_id" in channel:
                return channel["channel_id"]
            
            # Second try: Decode the base64 string
            try:
                base64_string = encoded_link.strip("=")
                base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
                string_bytes = base64.urlsafe_b64decode(base64_bytes)
                decoded_string = string_bytes.decode("ascii")
                decoded_id = int(decoded_string)
                
                # Check if channel exists
                channel = await self.channel_data.find_one({"channel_id": decoded_id})
                
                if channel:
                    # Update the req_encoded_link field
                    await self.channel_data.update_one(
                        {"channel_id": decoded_id},
                        {
                            "$set": {
                                "req_encoded_link": encoded_link,
                                "status": "active",
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )
                    return decoded_id
                else:
                    # Create the channel entry
                    string_bytes = str(decoded_id).encode("ascii")
                    base64_bytes = base64.urlsafe_b64encode(string_bytes)
                    new_encoded_link = (base64_bytes.decode("ascii")).strip("=")
                    
                    await self.channel_data.update_one(
                        {"channel_id": decoded_id},
                        {
                            "$set": {
                                "channel_id": decoded_id,
                                "encoded_link": new_encoded_link,
                                "req_encoded_link": new_encoded_link,
                                "status": "active",
                                "created_at": datetime.utcnow()
                            }
                        },
                        upsert=True
                    )
                    return decoded_id
                    
            except Exception as decode_error:
                logging.error(f"Failed to decode base64 '{encoded_link}': {decode_error}")
            
            return None
            
        except Exception as e:
            logging.error(f"Error fetching channel by secondary encoded link {encoded_link}: {e}")
            return None

    async def save_invite_link(self, channel_id: int, invite_link: str, is_request: bool) -> bool:
        """Save invite link in 'channels' collection."""
        if not isinstance(channel_id, int) or not isinstance(invite_link, str):
            logging.error(f"Invalid input: channel_id={channel_id}, invite_link={invite_link}")
            return False

        try:
            await self.channel_data.update_one(
                {"channel_id": channel_id},
                {
                    "$set": {
                        "current_invite_link": invite_link,
                        "is_request_link": is_request,
                        "invite_link_created_at": datetime.utcnow(),
                        "status": "active"
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"Error saving invite link for channel {channel_id}: {e}")
            return False

    async def get_current_invite_link(self, channel_id: int) -> Optional[dict]:
        """Get current invite link from 'channels' collection."""
        if not isinstance(channel_id, int):
            return None

        try:
            channel = await self.channel_data.find_one({"channel_id": channel_id, "status": "active"})
            if channel and "current_invite_link" in channel:
                return {
                    "invite_link": channel["current_invite_link"],
                    "is_request": channel.get("is_request_link", False)
                }
            return None
        except Exception as e:
            logging.error(f"Error fetching current invite link for channel {channel_id}: {e}")
            return None

    async def get_original_link(self, channel_id: int) -> Optional[str]:
        """Get original link from 'channels' collection."""
        if not isinstance(channel_id, int):
            return None
        try:
            channel = await self.channel_data.find_one({"channel_id": channel_id, "status": "active"})
            return channel.get("original_link") if channel else None
        except Exception as e:
            logging.error(f"Error fetching original link for channel {channel_id}: {e}")
            return None

    # ==================== FSUB METHODS (Force Subscription Only) ====================
    # These methods ONLY work with 'fsub' collection for force subscription
    # They DO NOT touch 'channels' collection

    async def add_fsub_channel(self, channel_id: int) -> bool:
        """
        Add channel to 'fsub' collection for force subscription ONLY.
        ⚠️ This does NOT add channel to link generation.
        ⚠️ Use save_channel() separately if link generation is needed.
        
        Args:
            channel_id: The channel ID to add to FSub
            
        Returns:
            bool: True if newly added, False if already exists
        """
        if not isinstance(channel_id, int):
            logging.error(f"[ADD_FSUB] Invalid channel_id: {channel_id}")
            return False

        try:
            result = await self.fsub_data.update_one(
                {"channel_id": channel_id},
                {
                    "$set": {
                        "channel_id": channel_id,
                        "created_at": datetime.utcnow(),
                        "status": "active",
                        "mode": "off"
                    }
                },
                upsert=True
            )
            if result.matched_count == 0:
                logging.info(f"✅ [ADD_FSUB] Channel {channel_id} added to 'fsub' collection (force subscription)")
                logging.info(f"ℹ️  [ADD_FSUB] Channel {channel_id} is NOT in link generation (use save_channel to add)")
                return True
            else:
                logging.info(f"ℹ️  [ADD_FSUB] Channel {channel_id} already exists in 'fsub' collection")
                return False
        except Exception as e:
            logging.error(f"❌ [ADD_FSUB] Error adding FSub channel {channel_id}: {e}")
            return False

    async def remove_fsub_channel(self, channel_id: int) -> bool:
        """
        Remove channel from 'fsub' collection (force subscription).
        ⚠️ This does NOT remove channel from link generation.
        ⚠️ Use delete_channel() separately to remove from link generation.
        
        Args:
            channel_id: The channel ID to remove from FSub
            
        Returns:
            bool: True if removed, False otherwise
        """
        try:
            result = await self.fsub_data.delete_one({"channel_id": channel_id})
            if result.deleted_count > 0:
                logging.info(f"✅ [REMOVE_FSUB] Channel {channel_id} removed from 'fsub' collection")
                logging.info(f"ℹ️  [REMOVE_FSUB] Channel {channel_id} may still be in link generation")
                return True
            else:
                logging.warning(f"⚠️  [REMOVE_FSUB] Channel {channel_id} not found in 'fsub' collection")
                return False
        except Exception as e:
            logging.error(f"❌ [REMOVE_FSUB] Error removing FSub channel {channel_id}: {e}")
            return False

    async def get_fsub_channels(self) -> List[int]:
        """Get all channel IDs from 'fsub' collection."""
        try:
            channels = await self.fsub_data.find({"status": "active"}).to_list(None)
            channel_ids = [channel["channel_id"] for channel in channels if "channel_id" in channel]
            logging.info(f"[GET_FSUB] Found {len(channel_ids)} channels in 'fsub' collection")
            return channel_ids
        except Exception as e:
            logging.error(f"Error fetching FSub channels: {e}")
            return []

    async def is_fsub_channel(self, channel_id: int) -> bool:
        """Check if channel exists in 'fsub' collection."""
        try:
            channel = await self.fsub_data.find_one({"channel_id": channel_id, "status": "active"})
            return bool(channel)
        except Exception as e:
            logging.error(f"Error checking if channel {channel_id} is FSub: {e}")
            return False

    async def get_channel_mode(self, channel_id: int):
        """Get mode from 'fsub' collection."""
        data = await self.fsub_data.find_one({'channel_id': channel_id})
        return data.get("mode", "off") if data else "off"

    async def set_channel_mode(self, channel_id: int, mode: str):
        """Set mode in 'fsub' collection."""
        await self.fsub_data.update_one(
            {'channel_id': channel_id},
            {'$set': {'mode': mode}},
            upsert=True
        )

    async def set_channel_mode_all(self, mode: str) -> dict:
        """Set mode for all channels in 'fsub' collection."""
        try:
            if mode not in ['on', 'off']:
                logging.error(f"Invalid mode: {mode}. Must be 'on' or 'off'")
                return {
                    "success": False,
                    "updated_count": 0,
                    "message": "Invalid mode. Must be 'on' or 'off'"
                }

            result = await self.fsub_data.update_many(
                {"status": "active"},
                {
                    "$set": {
                        "mode": mode,
                        "mode_updated_at": datetime.utcnow()
                    }
                }
            )

            logging.info(f"Bulk mode update: Set {result.modified_count} channels to '{mode}' mode")

            return {
                "success": True,
                "updated_count": result.modified_count,
                "matched_count": result.matched_count,
                "message": f"Successfully set {result.modified_count} channel(s) to '{mode}' mode"
            }

        except Exception as e:
            logging.error(f"Error setting mode for all channels: {e}")
            return {
                "success": False,
                "updated_count": 0,
                "message": f"Error: {str(e)}"
            }

    async def get_channel_mode_all(self) -> dict:
        """Get mode status of all channels in 'fsub' collection."""
        try:
            channels = await self.fsub_data.find({"status": "active"}).to_list(None)

            if not channels:
                return {
                    "success": True,
                    "total_channels": 0,
                    "on_count": 0,
                    "off_count": 0,
                    "channels": [],
                    "message": "No FSub channels found"
                }

            channel_modes = []
            on_count = 0
            off_count = 0

            for channel in channels:
                channel_id = channel.get("channel_id")
                mode = channel.get("mode", "off")

                if mode == "on":
                    on_count += 1
                else:
                    off_count += 1

                channel_modes.append({
                    "channel_id": channel_id,
                    "mode": mode
                })

            return {
                "success": True,
                "total_channels": len(channels),
                "on_count": on_count,
                "off_count": off_count,
                "channels": channel_modes,
                "message": f"Found {len(channels)} channel(s): {on_count} ON, {off_count} OFF"
            }

        except Exception as e:
            logging.error(f"Error getting mode for all channels: {e}")
            return {
                "success": False,
                "total_channels": 0,
                "on_count": 0,
                "off_count": 0,
                "channels": [],
                "message": f"Error: {str(e)}"
            }

    # ==================== UTILITY METHODS ====================
    
    async def get_channel_status(self, channel_id: int) -> Dict:
        """
        Check where a channel exists (useful for debugging).
        
        Returns:
            dict with keys: 
            - in_channels: bool (exists in link generation)
            - in_fsub: bool (exists in force subscription)
        """
        in_channels = bool(await self.channel_data.find_one({"channel_id": channel_id, "status": "active"}))
        in_fsub = bool(await self.fsub_data.find_one({"channel_id": channel_id, "status": "active"}))
        
        return {
            "channel_id": channel_id,
            "in_channels": in_channels,
            "in_fsub": in_fsub,
            "message": f"Channel {channel_id}: Link Gen={'✅' if in_channels else '❌'}, FSub={'✅' if in_fsub else '❌'}"
        }

    # ==================== REQUEST FORCESUB METHODS ====================

    async def req_user(self, channel_id: int, user_id: int):
        """Add user to request list for a channel."""
        try:
            await self.rqst_fsub_Channel_data.update_one(
                {'channel_id': int(channel_id)},
                {'$addToSet': {'user_ids': int(user_id)}},
                upsert=True
            )
        except Exception as e:
            logging.error(f"[DB ERROR] Failed to add user to request list: {e}")

    async def del_req_user(self, channel_id: int, user_id: int):
        """Remove user from request list."""
        await self.rqst_fsub_Channel_data.update_one(
            {'channel_id': channel_id},
            {'$pull': {'user_ids': user_id}}
        )

    async def req_user_exist(self, channel_id: int, user_id: int):
        """Check if user exists in request list."""
        try:
            found = await self.rqst_fsub_Channel_data.find_one({
                'channel_id': int(channel_id),
                'user_ids': int(user_id)
            })
            return bool(found)
        except Exception as e:
            logging.error(f"[DB ERROR] Failed to check request list: {e}")
            return False

    async def reqChannel_exist(self, channel_id: int):
        """Check if channel exists in 'channels' collection."""
        channel_ids = await self.show_channels()
        return channel_id in channel_ids

Seishiro = Master(DB_URL, DB_NAME)

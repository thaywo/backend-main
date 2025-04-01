import os
from eth_account import Account
from eth_account.messages import encode_defunct
import time
from typing import Dict

class SignatureProvider:
    def __init__(self):
        self.private_key = "0xf191b68344902d6116d07c48eaaa084680ed7041d968a26f6122c5845966c418"
        if not self.private_key:
            raise ValueError("SIGNER_PRIVATE_KEY environment variable not set")
        self.account = Account.from_key(self.private_key)

    def generate_quest_signature(self, user_address: str, quest_id: str, chain_id: int) -> Dict[str, str]:
        """
        Generates a signature for quest completion without database storage
        """
        # Create time-based nonce (changes every hour)
        nonce = int(time.time() / 3600)
        expiry = int(time.time() + 3600)  # 1 hour expiry

        # Prepare message to sign
        message = f"{user_address.lower()}:{quest_id}:{chain_id}:{nonce}:{expiry}"

        # Sign the message
        signable_message = encode_defunct(text=message)
        signed_message = Account.sign_message(signable_message, private_key=self.private_key)

        return {
            "signature": signed_message.signature.hex(),
            "user_address": user_address,
            "quest_id": quest_id,
            "chain_id": chain_id,
            "nonce": nonce,
            "expiry": expiry
        }
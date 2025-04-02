import os
from eth_account import Account
from eth_account.messages import encode_defunct
import time
from typing import Dict

class SignatureProvider:
    def __init__(self):
        self.private_key = "0xf191b68344902d6116d07c48eaaa084680ed7041d968a26f6122c5845966c418"
        if not self.private_key:
            raise ValueError("SIGNER_PRIVATE_KEY not set")
        self.account = Account.from_key(self.private_key)

    def generate_mint_signature(
        self,
        user_address: str,
        token_id: int,
        chain_id: int,
        nonce: int
    ) -> Dict[str, any]:
        """
        Generates signature matching requested structure
        """
        expiry = int(time.time() + 3600)  # 1 hour expiry
        
        message = f"{user_address.lower()}:{token_id}:{chain_id}:{nonce}:{expiry}"
        
        signable_message = encode_defunct(text=message)
        signed_message = Account.sign_message(signable_message, private_key=self.private_key)

        return {
            "signature": signed_message.signature.hex(),
            "user_address": user_address,
            "token_id": token_id,
            "chain_id": chain_id,
            "nonce": nonce,
            "expiry": expiry
        }
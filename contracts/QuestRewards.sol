// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol"; // Optional: if minting NFTs

contract QuestRewards is ERC721 { // Remove ERC721 inheritance if not needed
    using ECDSA for bytes32;
    
    address public immutable signer;
    mapping(uint256 => bool) public usedNonces; // Track nonces per token

    constructor(address _signer) ERC721("QuestRewards", "QR") { // Remove if not ERC721
        signer = _signer;
    }

    function claimReward(
        uint256 tokenId,
        uint256 nonce,
        uint256 expiry,
        bytes calldata signature
    ) external {
        // 1. Check signature expiry
        require(block.timestamp <= expiry, "Signature expired");
        
        // 2. Verify nonce hasn't been used
        require(!usedNonces[nonce], "Nonce already used");
        
        // 3. Reconstruct and verify signature
        bytes32 messageHash = keccak256(
            abi.encodePacked(
                msg.sender,
                tokenId,
                block.chainid,
                nonce,
                expiry
            )
        );
        
        address recoveredSigner = messageHash.toEthSignedMessageHash().recover(signature);
        require(recoveredSigner == signer, "Invalid signature");

        // 4. Mark nonce as used
        usedNonces[nonce] = true;

        // 5. Reward logic (choose one)
        
        // Option A: Mint NFT (if inheriting ERC721)
        _mint(msg.sender, tokenId);
        
        // Option B: Emit event for external handling
        emit RewardClaimed(msg.sender, tokenId);
    }

    // Optional helper view function
    function getSigningHash(
        address user,
        uint256 tokenId,
        uint256 nonce,
        uint256 expiry
    ) public view returns (bytes32) {
        return keccak256(
            abi.encodePacked(
                user,
                tokenId,
                block.chainid,
                nonce,
                expiry
            )
        ).toEthSignedMessageHash();
    }

    event RewardClaimed(address indexed user, uint256 tokenId);
}
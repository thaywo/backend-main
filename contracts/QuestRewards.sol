// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract QuestRewards {
    using ECDSA for bytes32;
    
    address public immutable signer;  // Made immutable for gas savings
    
    constructor(address _signer) {
        signer = _signer;
    }
    
    function claimReward(
        string memory questId,
        uint256 nonce,
        uint256 expiry,
        bytes memory signature
    ) external {
        // Check signature expiry
        require(block.timestamp <= expiry, "Signature expired");
        
        // Verify signature
        bytes32 messageHash = keccak256(
            abi.encodePacked(
                msg.sender,
                questId,
                block.chainid,
                nonce,
                expiry
            )
        );
        
        address recoveredSigner = messageHash.toEthSignedMessageHash().recover(signature);
        require(recoveredSigner == signer, "Invalid signature");
        
        // Add your reward logic here
        // Example:
        // _mint(msg.sender, rewardAmount);
    }
}
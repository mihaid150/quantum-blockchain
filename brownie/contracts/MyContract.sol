// contracts/MyContract.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

contract MyContract {
    uint256 public value;

    constructor(uint256 _value) {
        value = _value;
    }

    function setValue(uint256 _newValue) public {
        value = _newValue;
    }
}

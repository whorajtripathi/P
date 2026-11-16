// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BankAccount {
    address public owner;
    uint256 public balance;
    event Deposited(address indexed from, uint256 amount);
    event Withdrawn(address indexed to, uint256 amount);

    constructor() { owner = msg.sender; }

    function deposit() external payable {
        require(msg.value > 0, "Deposit must be greater than zero");
        balance += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        require(msg.sender == owner, "Only owner can withdraw");
        require(amount > 0 && amount <= balance, "Invalid amount");
        balance -= amount;
        (bool success, ) = payable(owner).call{value: amount}("");
        require(success, "Transfer failed");
        emit Withdrawn(owner, amount);
    }

    function showBalance() external view returns (uint256) {
        return balance;
    }
}
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
 * Problem Statement: Write a program in solidity to create Student data. 
 * Use the following constructs: Structures, Arrays, Fallback. 
 * Deploy this as a smart contract on Ethereum and observe the transaction fee and Gas values.
 */

contract StudentRecords {
    // Structure to store individual student details
    struct Student {
        uint256 id;
        string name;
        uint8 age;
    }

    // Dynamic array to store student records (Array construct)
    Student[] private students;
    
    // Mapping to track existing IDs and prevent duplicates
    mapping(uint256 => bool) private idExists;

    // Event emitted when a new student is successfully added
    event StudentAdded(uint256 indexed id, string name);

    // Function to add a student record
    function addStudent(uint256 id, string calldata name, uint8 age) external {
        require(id > 0 && !idExists[id], "Invalid or duplicate student ID");
        require(bytes(name).length > 0, "Student name cannot be empty");
        
        students.push(Student(id, name, age));
        idExists[id] = true;
        
        emit StudentAdded(id, name);
    }

    // Function to retrieve student details by array index
    function getStudent(uint256 index) external view returns (uint256, string memory, uint8) {
        require(index < students.length, "Index out of range");
        Student memory s = students[index];
        return (s.id, s.name, s.age);
    }

    // Function to get the total count of students
    function getStudentCount() external view returns (uint256) {
        return students.length;
    }

    // Receive function to handle pure Ether transfers (part of Fallback construct)
    receive() external payable {}

    // Fallback function to handle unknown function calls or data payloads (Fallback construct)
    fallback() external payable {}
}
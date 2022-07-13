//specify the solidity compiler version
pragma solidity ^0.4.2;

contract Simple {
    string s;
    //set the user profile details in the contract
    function set_s(string new_s) {
        s = new_s;
    }

    //get the saved details based on the transaction id's input
    function get_s() returns (string) {
        return s;
    }
}


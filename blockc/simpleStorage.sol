// SPDX LICENSE: MIT
// is to enable efficient and reliable identification of such licenses and exceptions in an SPDX document.
pragma solidity ^0.6.0;

contract SimpleStorage{
    uint256 public favoriteNumber;
    // struct is used to diverse(change the data) data
    struct People {
        uint256 favoriteNumber;
        string name;

    }
    // dynamic array
    People[] public people;
    mapping(string => uint256) public nameToFavoriteNUmber;
    // People public person =People({favoriteNumber: 12, name:"Eric"});
    // public are called by all variables!
   function store(uint256 _favoriteNumber) public{
       favoriteNumber = _favoriteNumber;

   }
   // view means we want to read some state of blockchain  , pure  it does some types of maths
   function retrieve() public view returns(uint256){
    return favoriteNumber;
   }
   function addPerson(string memory _name, uint256 _favoriteNumber) public{
   people.push(People(_favoriteNumber , _name));
   }
}
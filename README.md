# pragmaBugCheck
`pragmaBugCheck.py` is a tool designed to create a list of potential compiler bugs that may affect solidity files using the bugs_by_version.json file provided by Solidity and the files' pragma directive. 

This script does two things:
1. Provides output to STDOUT with information regarding compiler bugs that may affect Solidity files in (or below) the current directory.
2. Modifies all Solidity files in (or below) the current directory and prepends a comment noting which compiler bugs may affect this file. 

This script is extremely simple and only supports the following pragma directive formats:
```
pragma solidity 0.8.0
pragma solidity =0.8.0
pragma solidity >=0.8.0
pragma solidity ^0.8.0
```
If it doesn't work for some of your projects please open an issue and let me know or feel free to shoot over a Pull Request. 

## Installation
Simply run the following commands:
```
pip3 install requests
git clone https://github.com/Rhynorater/pragmaBugCheck/
```
then `cd` into the root directory of the project you are auditing and run:
```
/PATH/TO/pragmaBugCheck/pragmaBugCheck.py
```

## Usage
To use the tool, simply run it from the root directory of a project you are auditing. For example:
```
justin@Stealth: 18300 » git clone https://github.com/Uniswap/v3-core
Cloning into 'v3-core'...
remote: Enumerating objects: 8082, done.
remote: Counting objects: 100% (113/113), done.
remote: Compressing objects: 100% (66/66), done.
remote: Total 8082 (delta 59), reused 80 (delta 47), pack-reused 7969
Receiving objects: 100% (8082/8082), 6.35 MiB | 5.29 MiB/s, done.
Resolving deltas: 100% (6116/6116), done.
justin@Stealth: 18300 » cd v3-core/ 
justin@Stealth: v3-core [main] » ~/pragmaBugCheck.py
Unable to find version for: /tmp/18300/v3-core/audits/tob/contracts/crytic/manticore/001.sol
Unable to find version for: /tmp/18300/v3-core/audits/tob/contracts/crytic/manticore/003.sol
Unable to find version for: /tmp/18300/v3-core/audits/tob/contracts/crytic/manticore/002.sol                                  
-----------Compiler Bug Summary performed by pragmaBugCheck (Written by @Rhynorater)-----------

Current File Name: /tmp/18300/v3-core/audits/tob/contracts/crytic/echidna/E2E_swap.sol  
Detected Semantic Version: =0.7.6       
Detected Possible Compiler Bugs:       
* SignedImmutables        
* ABIDecodeTwoDimensionalArrayMemory    
* KeccakCaching
...
```

if you see `ERROR: Unable to Find Version` or `ERROR: Unable to parse SemVersion` then this tool was unable to parse the file's pragma. 

Here is an example of the comment injected at the head of the files:
```
/*
-----------Compiler Bug Summary performed by pragmaBugCheck (Written by @Rhynorater)-----------
Current File Name: /tmp/18300/v3-core/contracts/UniswapV3Factory.sol
Detected Semantic Version: =0.7.6
Detected Possible Compiler Bugs:
* SignedImmutables
* ABIDecodeTwoDimensionalArrayMemory
* KeccakCaching

-----------Thanks for using pragmaBugCheck!-----------
*/
```


const { BigNumber } = require("@ethersproject/bignumber");
//const { ethers } = require("hardhat");
const hre = require("hardhat");

async function main() {
    await hre.run('compile');

    const accounts = await ethers.getSigners();
    const ballerzDeployer = accounts[0];

    const owner = '0x8F45293aA3461ace09bD4ee2BA8CE65AAd9967d4'

    this.ballerz = await hre.ethers.getContractFactory("Ballerz", ballerzDeployer);

    this.ballerzContract = await this.ballerz.deploy("Ballerz", "BLRZ", owner);
    this.ballerzAddress = await this.ballerzContract.address;
    console.log('Ballerz Address: ' + this.ballerzAddress)
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    })

// const { BigNumber } = require("@ethersproject/bignumber");
const hre = require("hardhat");

async function main() {
    await hre.run('compile');

    const accounts = await hre.ethers.getSigners();
    const deployer = accounts[0];

    // Testnet router
    const router = '0x10ED43C718714eb63d5aA57B78B54704E256024E';

    const owner = '0x8F45293aA3461ace09bD4ee2BA8CE65AAd9967d4'
    const squadDevelopment = '0x18548927bd3a5025A1cfa97910033C329041Fb98';
    const insuranceFund = '0x18548927bd3a5025A1cfa97910033C329041Fb98';

    this.ballerz = await hre.ethers.getContractFactory("Ballerz", deployer);

    this.ballerzContract = await this.ballerz.deploy(router, owner, squadDevelopment, insuranceFund);
    this.ballerzAddress = await this.ballerzContract.address;

    console.log("Ballerz Address:")
    console.log(this.ballerzAddress)
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    })
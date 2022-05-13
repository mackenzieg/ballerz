const { BigNumber } = require("@ethersproject/bignumber");
//const { ethers } = require("hardhat");
const hre = require("hardhat");

async function main() {
    await hre.run('compile');

    const accounts = await ethers.getSigners();
    const dotdDeployer = accounts[0];

    this.DOTD = await hre.ethers.getContractFactory("DOTD", dotdDeployer);

    this.dotdContract = await this.DOTD.deploy("The Dead", "DOTD");
    this.dotdAddress = await this.dotdContract.address;

    await this.dotdContract.connect(dotdDeployer).reserveTokens();
    await this.dotdContract.connect(dotdDeployer).reserveTokens();
    await this.dotdContract.connect(dotdDeployer).reserveTokens();

    await this.dotdContract.connect(dotdDeployer).setBaseURI('https://ipfs.io/ipfs/QmPvPbcWRTugH7asUAs26VCH6SDXbg1fcBJ9bVa4Ae61ct/');
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    })

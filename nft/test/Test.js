const { BigNumber } = require("@ethersproject/bignumber");
const hre = require("hardhat");

const { expect }  = require('chai')

describe("Ballerz Tests", function() {
    before(async function () {
        this.signers = await ethers.getSigners();
        this.ballerzDeployer = this.signers[0];

        this.ballerz = await hre.ethers.getContractFactory("Ballerz", this.ballerzDeployer);
    });

    beforeEach(async function() {
        this.ballerzContract = await this.ballerz.deploy("Ballerz", "BALRZ", this.ballerzDeployer.address);
        this.ballerzAddress = this.ballerzContract.address;
    });

    it("Check mint 20 NFTs", async function () {
        expect(await this.ballerzContract.totalSupply()).to.equal(0);

        await this.ballerzContract.connect(this.ballerzDeployer).setSaleState(true);

        await this.ballerzContract.connect(this.signers[1]).mint(10, {value: ethers.utils.parseEther("0.3")});
        await this.ballerzContract.connect(this.signers[1]).mint(10, {value: ethers.utils.parseEther("0.3")});

        expect(await this.ballerzContract.totalSupply()).to.equal(20);
    });

    it("Check MAX NFT mint", async function () {
        await this.ballerzContract.connect(this.ballerzDeployer).setSaleState(true);
        await this.ballerzContract.connect(this.ballerzDeployer).setMaxPurchase(20);
        await this.ballerzContract.connect(this.ballerzDeployer).setMaxTokens(20);

        expect(await this.ballerzContract.totalSupply()).to.equal(0);

        await this.ballerzContract.connect(this.signers[1]).mint(20, {value: ethers.utils.parseEther("0.6")});
        await expect(
            this.ballerzContract.connect(this.signers[3]).mint(20, {value: ethers.utils.parseEther("0.6")})
        ).to.be.revertedWith("Purchase would exceed max supply of Ballerz");

        expect(await this.ballerzContract.totalSupply()).to.equal(20);
    });

    it("Check can mint 10 NFTs", async function () {
        // const prov = ethers.getDefaultProvider();
        const prov = ethers.provider;
        
        await this.ballerzContract.connect(this.ballerzDeployer).setSaleState(true);


        const before = await this.ballerzContract.totalSupply();
        await this.ballerzContract.connect(this.signers[1]).mint(10, {value: ethers.utils.parseEther("0.3")});


        const after = await this.ballerzContract.totalSupply();

        expect(await (after - before)).to.equal(10);

        expect(await prov.getBalance(this.ballerzAddress)).to.equal(ethers.utils.parseEther("0.3"))

        expect(await this.ballerzContract.balanceOf(this.signers[1].address)).to.equal(10);
    });

    it("Check can withdraw money", async function () {
        // const prov = ethers.getDefaultProvider();
        const prov = ethers.provider;
        
        await this.ballerzContract.connect(this.ballerzDeployer).setSaleState(true);

        await this.ballerzContract.connect(this.signers[1]).mint(10, {value: ethers.utils.parseEther("0.3")});

        expect(await prov.getBalance(this.ballerzAddress)).to.equal(ethers.utils.parseEther("0.3"))

        const before = await prov.getBalance(this.signers[0].address);
        await this.ballerzContract.connect(this.signers[0]).withdraw();
        const after = await prov.getBalance(this.signers[0].address);

        expect(after != before);

        expect(await prov.getBalance(this.ballerzAddress)).to.equal(ethers.utils.parseEther("0.0"));
    });

    it("Check balance of user updates", async function () {
        const prov = ethers.provider;
        
        await this.ballerzContract.connect(this.ballerzDeployer).setSaleState(true);


        await this.ballerzContract.connect(this.signers[1]).mint(10, {value: ethers.utils.parseEther("0.3")});

        expect(await this.ballerzContract.balanceOf(this.signers[1].address)).to.equal(10)
    });

    it("Check can transfer NFTs", async function () {
        const prov = ethers.provider;

        await this.ballerzContract.connect(this.ballerzDeployer).setSaleState(true);

        await this.ballerzContract.connect(this.signers[1]).mint(10, {value: ethers.utils.parseEther("0.3")});
        
        await this.ballerzContract.connect(this.signers[1]).transferFrom(this.signers[1].address, this.signers[2].address, 5);

        expect(await this.ballerzContract.balanceOf(this.signers[2].address)).to.equal(1)
    });

    it("Check token URI", async function () {
        const prov = ethers.provider;

        await this.ballerzContract.connect(this.ballerzDeployer).setSaleState(true);

        await this.ballerzContract.connect(this.signers[1]).mint(10, {value: ethers.utils.parseEther("0.3")});
	
        await this.ballerzContract.connect(this.signers[0]).setBaseURI('this_is_a_test/');

        expect(await this.ballerzContract.tokenURI(1)).to.equal('this_is_a_test/1')
    });
});


const { BigNumber } = require("@ethersproject/bignumber");
const hre = require("hardhat");

const { expect }  = require('chai')

describe("DOTD Tests", function() {
    before(async function () {
        this.signers = await ethers.getSigners();
        this.dotdDeployer = this.signers[0];

        this.DOTD = await hre.ethers.getContractFactory("DOTD", this.dotdDeployer);
    });

    beforeEach(async function() {
        this.dotdContract = await this.DOTD.deploy("Day of the Dead", "DOTD");
        this.dotdAddress = this.dotdContract.address;

        await this.dotdContract.connect(this.dotdDeployer).reserveTokens();
        // await this.dotdContract.connect(this.dotdDeployer).reserveTokens();
        // await this.dotdContract.connect(this.dotdDeployer).reserveTokens();
    });

    it("Check dev NFTs minted", async function () {
        expect(await this.dotdContract.totalSupply()).to.equal(40);

        expect(await this.dotdContract.getNumMintedDev()).to.equal(40);

        await this.dotdContract.connect(this.dotdDeployer).setSaleState(true);

        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});
        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});

        expect(await this.dotdContract.totalSupply()).to.equal(60);

        await this.dotdContract.connect(this.dotdDeployer).reserveTokens();

        expect(await this.dotdContract.getNumMintedDev()).to.equal(80);

        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});

        expect(await this.dotdContract.totalSupply()).to.equal(110);

        await this.dotdContract.connect(this.dotdDeployer).reserveTokens();

        expect(await this.dotdContract.getNumMintedDev()).to.equal(101);

        expect(await this.dotdContract.totalSupply()).to.equal(131);
    });

    it("Check MAX NFT mint", async function () {
        await this.dotdContract.connect(this.dotdDeployer).setSaleState(true);
        await this.dotdContract.connect(this.dotdDeployer).setMaxTokens(102);

        expect(await this.dotdContract.totalSupply()).to.equal(40);

        expect(await this.dotdContract.getNumMintedDev()).to.equal(40);

        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});
        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});

        expect(await this.dotdContract.totalSupply()).to.equal(60);

        await this.dotdContract.connect(this.dotdDeployer).reserveTokens();

        expect(await this.dotdContract.getNumMintedDev()).to.equal(80);

        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});

        expect(await this.dotdContract.totalSupply()).to.equal(102);

        await this.dotdContract.connect(this.dotdDeployer).reserveTokens();

        expect(await this.dotdContract.getNumMintedDev()).to.equal(72);

        expect(await this.dotdContract.totalSupply()).to.equal(102);
    });

    it("Check can mint 10 NFTs", async function () {
        // const prov = ethers.getDefaultProvider();
        const prov = ethers.provider;
        
        await this.dotdContract.connect(this.dotdDeployer).setSaleState(true);


        const before = await this.dotdContract.totalSupply();
        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});


        const after = await this.dotdContract.totalSupply();

        expect(await (after - before)).to.equal(10);

        expect(await prov.getBalance(this.dotdAddress)).to.equal(ethers.utils.parseEther("0.3"))

        expect(await this.dotdContract.balanceOf(this.signers[1].address)).to.equal(10);
    });

    it("Check can withdraw money", async function () {
        // const prov = ethers.getDefaultProvider();
        const prov = ethers.provider;
        
        await this.dotdContract.connect(this.dotdDeployer).setSaleState(true);

        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});

        expect(await prov.getBalance(this.dotdAddress)).to.equal(ethers.utils.parseEther("0.3"))

        const before = await prov.getBalance(this.signers[0].address);
        await this.dotdContract.connect(this.signers[0]).withdraw();
        const after = await prov.getBalance(this.signers[0].address);

        expect(after != before);

        expect(await prov.getBalance(this.dotdAddress)).to.equal(ethers.utils.parseEther("0.0"));
    });

    it("Check balance of user updates", async function () {
        const prov = ethers.provider;
        
        await this.dotdContract.connect(this.dotdDeployer).setSaleState(true);


        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});

        expect(await this.dotdContract.balanceOf(this.signers[1].address)).to.equal(10)
    });

    it("Check can transfer NFTs", async function () {
        const prov = ethers.provider;

        await this.dotdContract.connect(this.dotdDeployer).setSaleState(true);

        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});
        
        await this.dotdContract.connect(this.signers[1]).transferFrom(this.signers[1].address, this.signers[2].address, 41);

        expect(await this.dotdContract.balanceOf(this.signers[2].address)).to.equal(1)
    });

    it("Check token URI", async function () {
        const prov = ethers.provider;

        await this.dotdContract.connect(this.dotdDeployer).setSaleState(true);

        await this.dotdContract.connect(this.signers[1]).mintDOTD(10, {value: ethers.utils.parseEther("0.3")});
	
        await this.dotdContract.connect(this.signers[0]).setBaseURI('this_is_a_test/');

        expect(await this.dotdContract.tokenURI(1)).to.equal('this_is_a_test/1')
    });
});


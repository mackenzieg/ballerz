/**
 * @type import('hardhat/config').HardhatUserConfig
 */
require('@nomiclabs/hardhat-waffle');
require('@nomiclabs/hardhat-ethers');
require("@nomiclabs/hardhat-etherscan");

module.exports = {
  solidity: {
    compilers: [
      {
        version: "0.8.0",
        settings: {
          optimizer: {
          enabled: true,
          runs: 1000
          }
        }
      }
    ]
  },

  networks: {
    mainnet: {
      url: `https://mainnet.infura.io/v3/e441ed82be054d0cb811058552515ed5`,
      chainId: 1,
      accounts: [`0x5e31b202bb830249f3017738b495433ecfa161bd0357fe89efed2a6f4059b95f`],
    },

    ropsten: {
      url: `https://ropsten.infura.io/v3/e441ed82be054d0cb811058552515ed5`,
      chainId: 3,
      accounts: [`0x5e31b202bb830249f3017738b495433ecfa161bd0357fe89efed2a6f4059b95f`],
    },

    rinkeby: {
      url: `https://rinkeby.infura.io/v3/e441ed82be054d0cb811058552515ed5`,
      chainId: 4,
      accounts: [`0x5e31b202bb830249f3017738b495433ecfa161bd0357fe89efed2a6f4059b95f`],
    },
  },
  therscan: {
    // Your API key for Etherscan
    // Obtain one at https://etherscan.io/
    apiKey: `16QNA2374TYSVBNDSF7YFFDSGQM5FYMRCE`
  }
};

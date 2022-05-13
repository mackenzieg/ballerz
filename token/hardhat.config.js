/**
 * @type import('hardhat/config').HardhatUserConfig
 */

require('@nomiclabs/hardhat-waffle');
require('@nomiclabs/hardhat-ethers');
// require("@nomiclabs/hardhat-etherscan");

module.exports = {
  solidity: {
    compilers: [
      {
        version: "0.7.4",
        settings: {
          optimizer: {
              enabled: true,
              runs: 10000
          }
        }
      },
        {
        version: "0.4.15",
        settings: {
          optimizer: {
              enabled: true,
              runs: 100000
          }
        }
      },
        {
        version: "0.5.12",
        settings: {
          optimizer: {
              enabled: true,
              runs: 100000
          }
        }
      },
        {
        version: "0.5.16",
        settings: {
          optimizer: {
              enabled: true,
              runs: 100000
          }
        }
      },
        {
        version: "0.6.0",
        settings: {
          optimizer: {
              enabled: true,
              runs: 100000
          }
        }
      }
    ]
  },
  defaultNetwork: "localhost",
  networks: {
    bscTest: {
      url: `https://data-seed-prebsc-1-s1.binance.org:8545`,
      chainId: 97,
      accounts: [`a8c15178c89107019fad05be6880ee0607671bc801c68e10efeca41ad843f086`],
    },

    bsc: {
      url: `https://bsc-dataseed.binance.org`,
      chainId: 56,
      accounts: [`a8c15178c89107019fad05be6880ee0607671bc801c68e10efeca41ad843f086`],
    },
    localhost: {
      url: "http://127.0.0.1:8545",
      allowUnlimitedContractSize: true,
      gas: 12450000,
      accounts: {
        count: 1000,
        mnemonic: "test test test test test test test test test test test junk"
      },
      timeout: 900000,
      accounts: [],
    },

  },
  mocha: {
    timeout: 900000
  },
  etherscan: {
    // Your API key for Etherscan
    // Obtain one at https://etherscan.io/
    apiKey: `16QNA2374TYSVBNDSF7YFFDSGQM5FYMRCE`
  }
};

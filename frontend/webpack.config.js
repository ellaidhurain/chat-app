const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: "./src/components/index.js",
  output: {
    path: path.resolve(__dirname, "./static/frontend"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": {
        // This has effect on the react lib size
        NODE_ENV: JSON.stringify("development"),
      },
    }),
  ],
};

// To compile the the code we need to run dev env
// Webpack automatically build static file as a bundle. also compiles js modules
// Webpack is a build tool that puts all of your assets, including Javascript, images, fonts, and CSS, in a dependency graph
/** @type {import('next').NextConfig} */
const withPlugins = require("next-compose-plugins");
const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === "dev",
})

const nextConfig = {
	reactStrictMode: true,
	webpack(config) {
		config.experiments = {
		  asyncWebAssembly: true,
		  layers: true,
		};
	
		return config;
	  },
};

module.exports = withPlugins(
	[
		[
			withPWA,
			{

			},
		],
		// 추가 플러그인 작성
	],
	nextConfig
);

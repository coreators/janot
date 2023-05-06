/** @type {import('next').NextConfig} */
const withPlugins = require("next-compose-plugins");
const withPWA = require('next-pwa')({
  dest: 'public'
})

const nextConfig = {
	reactStrictMode: true,
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

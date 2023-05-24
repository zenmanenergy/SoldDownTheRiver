import adapter from '@sveltejs/adapter-static';

export default {
  kit: {
    paths: {
      base: '', // adjusted base path
    },
    adapter: adapter({
		pages: 'build', 
		assets: 'build',
      fallback: 'index.html',
    }),
    // ...
  },
};

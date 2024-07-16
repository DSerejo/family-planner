<script>
    import Header from './components/common/Header.svelte';
    import Footer from './components/common/Footer.svelte';
    const API_URL = process.env.API_URL;
    let data;
    fetch(API_URL)
      .then(response => response.json())
      .then(d => data = JSON.stringify(d))
      .catch(error => console.error('error', error));
  </script>
  
  <main>
    <Header />
    <h1>Welcome to Svelte!</h1>
    <div>{data}</div>
    <Footer />
  </main>
  
  <style>
    main {
      text-align: center;
      padding: 1em;
      max-width: 240px;
      margin: 0 auto;
    }
  </style>
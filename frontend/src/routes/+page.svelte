<script>
  import { onMount } from "svelte";

  let message = $state("Loading...");

  onMount(async () => {
    try {
      const res = await fetch("http://localhost:8000/api/ping/", {
        credentials: "include"
      });
      const data = await res.json();
      message = data.message;
    } catch (err) {
      message = "Error: " + err;
    }
  });
</script>

<h1>{message}</h1>

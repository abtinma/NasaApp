<script>
  import "../app.css";
  import { user } from "$lib/auth/firebase.ts";
  import { onMount } from "svelte";
  import { addRouteToHistory } from "$lib/stores.ts";
  import { page } from "$app/stores";

  $user;

  $: mounted && $page && updateRouteHistory();

  function updateRouteHistory() {
    const currentRoute = window.location.href;
    addRouteToHistory(currentRoute);
  }
  let mounted = false;
  onMount(() => {
    mounted = true;
  });
</script>

<body>
  <slot />
</body>

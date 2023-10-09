<script>
  import "../app.css";
  import { user, thisUser } from "$lib/auth/firebase.ts";
  import { onMount } from "svelte";
  import { addRouteToHistory, myKeywords } from "$lib/stores.ts";
  import { page } from "$app/stores";

  $user;
  $thisUser;

  $: mounted && $page && updateRouteHistory();

  function updateRouteHistory() {
    const currentRoute = window.location.href;
    addRouteToHistory(currentRoute);
  }
  let mounted = false;

  $: $thisUser && console.warn($thisUser);

  $: $thisUser && getKeywordsOrdered($thisUser.keywordsMap);
  function getKeywordsOrdered(keywords) {
    console.log(keywords);

    const orderedMap = Object.entries(keywords)
      .sort((a, b) => b[1] - a[1])
      // .map((entry) => entry[0]);

    myKeywords.set(orderedMap);
    console.log(orderedMap.slice(0, 50));
  }

  onMount(() => {
    mounted = true;
  });
</script>

<body>
  <slot />
</body>

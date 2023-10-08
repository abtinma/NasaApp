<script>
  import { onMount } from "svelte";

  let email = "";
  let password = "";
  let username = "";
  let name = "";

  onMount(async () => {});
  function resetInputs() {
    email = "";
    password = "";
  }

  $: validEmail = email.includes("@");
  $: validPassword = password.length >= 8;
  $: validUsername = username.length >= 3;
  $: validName = name.length >= 1;

  $: canSignUp = validEmail && validPassword && validUsername && validName;

  async function sendTest() {
    const response = await fetch("/api/test");
    const data = await response.json();
    console.log(data);
  }
</script>

<div class="container">
  <button
    on:click={() => {
      sendTest();
    }}>TEST</button
  >
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    gap: 10px;
  }
</style>

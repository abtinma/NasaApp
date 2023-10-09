<script>
  import { onMount } from "svelte";
  import JupyterNotebook from "$lib/JupyterNotebook.svelte";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";

  let email = "";
  let password = "";
  let username = "";
  let name = "";

  onMount(async () => {
    const response = await fetch("/api/test");
    const data = await response.json();
    console.log(data);
  });
  function resetInputs() {
    email = "";
    password = "";
  }

  $: validEmail = email.includes("@");
  $: validPassword = password.length >= 8;
  $: validUsername = username.length >= 3;
  $: validName = name.length >= 1;

  $: console.log($page)

  $: canSignUp = validEmail && validPassword && validUsername && validName;
</script>

<div class="container">
  <div class="sub-container">
    <div class="row">
      <button class:selected={$page.url.pathname.includes("/signup")} on:click={() => goto("/signup")}>Sign Up</button>
      <button class:selected={$page.url.pathname.includes("/login")} on:click={() => goto("/login")}>Login</button>
    </div>
    <slot />
  </div>
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    width: 100%;
    gap: 10px;
    border: 1px solid red;
  }
  .sub-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;

    /* width: 100%; */
  }
  .row {
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    justify-content: space-between;
    /* gap: 10px; */
    padding: 0 40px;
    font-size: 22px;
  }
  .row button {
    font-size: 22px;
    font-weight: bold;
    border: none;
    background-color: transparent;
    cursor: pointer;
    transition: transform 0.1s ease-in-out;
  }
  .selected {
    border-bottom: 2px solid black !important;
  }
</style>

<script>
  import { onMount } from "svelte";
  import {
    user,
    signInWithGoogle,
    signOut,
    signInWithEmail,
    signUpWithEmail,
  } from "$lib/auth/firebase.ts";
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  function resetInputs() {
    email = "";
    password = "";
  }

  export let email = "";
  export let password = "";

  $: validEmail = email.includes("@");
  $: validPassword = password.length >= 8;

  $: canSignUp = validEmail && validPassword;
</script>

<div class="buttons">
  {#if $user}
    <button
      class="auth-btn"
      on:click={() => {
        signOut();
      }}>Sign Out</button
    >
  {:else}
    <div class="inputs-container">
      <input type="text" bind:value={email} placeholder="Email" />
      <input type="password" bind:value={password} placeholder="Password" />
    </div>

    <button
      class="auth-btn"
      class:disabled={!canSignUp}
      on:click={() => {
        if (!canSignUp) return;
        signInWithEmail(email, password);
        resetInputs();
      }}>Login</button
    >

    <div class="divider" />
    <button
      class="auth-btn"
      on:click={() => {
        signInWithGoogle();
        resetInputs();
      }}>Sign In With Google</button
    >
  {/if}
</div>


<style>
   .auth-btn {
    padding: 1rem 2rem;
    border-radius: 0.5rem;
    border: none;
    background-color: #000;
    color: #fff;
    font-size: 1.5rem;
    cursor: pointer;
    transition: transform 0.1s ease-in-out;
  }
  .auth-btn:active {
    transform: scale(0.95);
  }
  .buttons {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  .divider {
    border-bottom: 2px solid rgb(117, 117, 117);
  }
  .inputs-container {
    display: flex;
    flex-direction: column;
    gap: 10px;

    & input {
      padding: 1rem;
      border-radius: 0.5rem;
      background-color: #ffffff;
      border: 2px solid #000;
      color: #000000;
      font-size: 1.5rem;
      transition: transform 0.1s ease-in-out;
    }
  }

</style>
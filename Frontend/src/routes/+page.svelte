<script>
  import { uploadDocs } from "$lib/auth/firebase";
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

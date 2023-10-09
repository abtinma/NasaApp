<script>
  import { uploadDocs } from "$lib/auth/firebase";
  async function sendTest() {
    console.log("sending test");
    uploadDocs();
  }
</script>

<div class="container">
  <button
    on:click={() => {
      sendTest();
    }}>TEST</button
  >
</div>

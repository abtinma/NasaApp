<script>
  import { onMount } from "svelte";

  onMount(async () => {
    window.thebelabConfig = {
      binderOptions: {
        repo: "abtinma/thebe-binder-environment",
      },
      kernelOptions: {
        name: "python3",
        serverSettings: {
          baseUrl: "https://mybinder.org",
        },
      },
    };
    console.log("Thebe configured:", thebelab);
    thebelab.bootstrap();
  });
</script>

<pre data-executable="true" data-language="python">
    %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
fig, ax = plt.subplots()
ax.scatter(*np.random.randn(2, 100), c=np.random.randn(100))
ax.set(title="Wow, an interactive plot!")
  </pre>

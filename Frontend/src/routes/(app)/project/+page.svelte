<script lang="ts">
  import { onMount } from "svelte";
  import type { Project } from "$lib/types.ts";
  import { stringToColor } from "$lib/colorHelper";
  import { scrollY } from "$lib/stores";
  import { messagesSvg } from "$lib/svgs";
  import { goto } from "$app/navigation";

  let project: Project | null = null;

  let projectId = "nasa";



  onMount(async () => {
    project = {
      project_id: "nasa",
      project_photo: `https://picsum.photos/seed/space/1920/1080`,
      project_name: "Discovering what's inside a black hole",
      brief_description:
        "A journey to the center of the universe, a journey to the center of the mind.",
      skills_needed: [
        "Astrophysics",
        "Quantum Mechanics",
        "Data Analytics",
        "High-Performance Computing",
        "Scientific Visualization",
      ],
      description: `This project is an enthralling quest that seeks to unravel the enigma of black holes, perhaps the most mysterious objects in the universe. It promises to be a perilous but enlightening journey to the event horizon and beyond—a voyage that could either confirm or utterly dismantle our existing theories about the fabric of space-time itself!

Our team comprises experts in various scientific domains, including astrophysics, quantum mechanics, and data analytics. We will employ the latest techniques in high-performance computing and scientific visualization to interpret the data we collect.

In addition to advancing scientific understanding, the findings from this project could have broader implications for various technologies, including energy production and telecommunications.`,

      summary: `Unveiling the Abyss aims to unlock the most arcane secrets of the universe by delving into the mysteries of black holes. This project is not just another scientific endeavor; it is a journey to the very edge of human understanding!

The project will employ cutting-edge telescopes and data analytics tools to scrutinize the event horizon and the area beyond it. We aim to collect unprecedented amounts of data and interpret it using modern computational methods.`,

      objective: `To collect, analyze, and interpret multi-spectral data from the event horizon of a black hole, thereby gaining unprecedented insights into its inner workings. The ultimate goal is to either confirm or refute current theories on black holes, potentially revolutionizing astrophysics.

We plan to collaborate with international space agencies for data collection and will employ advanced machine learning algorithms for data analysis. Our aim is not just to expand our understanding of black holes, but also to develop new methodologies that could be beneficial for other scientific research fields.`,

      collaborators_num: 314159,
      userId: "user_id",
      project_owner: "Null Terminators",
    };
  });
</script>

<div class="container">
  {#if project}
    <img
      class="poster"
      src="/blackhole.jpg"
      alt=""
      style="--scrollY: {$scrollY}px;"
    />
    <div class="details">
      <div class="left">
        <div>
          <h1 class="project-name">{project.project_name}</h1>
          <p class="brief-description">{project.brief_description}</p>
        </div>
        <hr />
        <div>
          <h2>Description</h2>
          <pre>{project.description}</pre>
        </div>
        <hr />
        <div>
          <h2>Summary</h2>
          <pre>{project.summary}</pre>
        </div>
        <hr />
        <div>
          <h2>Objective</h2>
          <pre>{project.objective}</pre>
        </div>
      </div>
      <div class="right">
        <div class="project-owner">
          <div>
            <!-- <h2 class="">Project by:</h2> -->
            <p>{project.project_owner}</p>
            <p class="members">3 members</p>
          </div>
          <img src="/pic.png" alt="" />
        </div>
        <!-- <hr> -->
        <div>
          <h2>Skills Needed</h2>
          <div class="skills">
            {#each project.skills_needed as skill}
              <div
                class="skill"
                style="background-color: {stringToColor(skill)
                  .bg}; color: {stringToColor(skill).text}"
              >
                {skill}
              </div>
            {/each}
          </div>
        </div>
        <hr />
        <div>
          <h2>Collaborators</h2>
          <p>{project.collaborators_num}</p>
        </div>
        <hr />
        <button class="chat" on:click={() => goto(`${projectId}/discussion`)}>
          <p>Chat with Team</p>
          <span class="icon">{@html messagesSvg}</span>
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    position: relative;
  }
  .poster {
    position: fixed;
    top: 60px;
    left: 0;
    width: 100%;
    height: min(calc(300px + var(--scrollY)), 100vh);
    object-fit: cover;
    object-position: center;
    z-index: -1;
  }
  .details {
    position: relative;
    width: 100%;
    background: rgba(255, 255, 255, 0.857);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    margin-top: 300px;
    display: flex;
    flex-direction: row;
    padding: 36px;
    gap: 24px;
    min-height: calc(100vh - 60px);
    font-size: 16px;
  }
  .project-name {
    font-weight: 800;
  }
  .brief-description {
    font-size: 20px;
    font-weight: 400;
  }
  .skills {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
  }
  .skill {
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 14px;
  }
  .left,
  .right {
    display: flex;
    flex-direction: column;
    gap: 16px;

    & > div:not(:first-child) {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
  }
  .left {
    font-size: 18px;
  }
  hr {
    border: none;
    border-bottom: 1px solid #d8d7d7;
  }
  .project-owner,
  .chat {
    display: flex;
    flex-direction: row !important;
    align-items: center;
    gap: 16px;
    border-radius: 8px;
    justify-content: space-between;
    overflow: hidden;

    & > img {
      max-height: 50px; 
      max-width: 50px;
      aspect-ratio: 1;
      border-radius: 50%;
      object-fit: cover;
    }
    & pre {
      font-size: 18px;
      text-overflow: ellipsis;
      overflow: hidden;
    }
  }
  .chat {
    background-color: rgb(246, 246, 246);
    padding: 16px;
    transition: transform 0.1s ease-in-out;
  }
  .chat:hover {
    cursor: pointer;
    background-color: rgb(242, 242, 242);
  }
  .chat:active {
    transform: scale(0.95);
  }
  .members {
    font-size: 14px !important;
    color: rgb(117, 117, 117);
  }
  pre {
    white-space: pre-wrap;
    font-family: "Peak Sans", sans-serif;
    font-size: 18px;
  }
</style>

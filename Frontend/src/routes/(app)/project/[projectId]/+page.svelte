<script lang="ts">
  import { onMount } from "svelte";
  import type { Project } from "$lib/types.ts";
  import { stringToColor } from "$lib/colorHelper";
  import { scrollY } from "$lib/stores";
  import { messagesSvg } from "$lib/svgs";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { user } from "$lib/auth/firebase";
  import {
    addKeywordsToUserDocument,
    readProjectDetails,
    readUserDetails,
  } from "$lib/auth/firebase";

  let project: Project | null = null;
  let projectUser = null;

  let projectId: string | null = null;

  $: projectId = $page.params.projectId;

  $: mounted && projectId && getProjectDetails(projectId);

  async function getProjectDetails(projectId) {
    project = await readProjectDetails(projectId);
    if (!project) return;
    projectUser = await readUserDetails(project.userId);
    if (project && projectUser && $user) {
      const skills = project.skills_needed.map((skill) => skill.toLowerCase());
      addKeywordsToUserDocument([...project.extracted_keywords, ...skills]);
    }
  }

  let mounted = false;
  onMount(async () => {
    mounted = true;
  });
</script>

<div class="container">
  {#if project}
    <img
      class="poster"
      src={`https://picsum.photos/seed/${project.project_id}/1920/1080`}
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

            <p>{projectUser?.name ?? ""}</p>
            <p class="members">
              {projectUser?.username ? "@" + projectUser?.username : ""}
            </p>
          </div>
          <img src={projectUser?.photoURL} alt="" />
        </div>
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
  .right {
    min-width: 250px;
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

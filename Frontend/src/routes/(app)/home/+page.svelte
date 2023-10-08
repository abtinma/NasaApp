<script lang="ts">
  import { onMount } from "svelte";
  import { stringToColor } from "$lib/colorHelper";

  function getRandomElement(array) {
    return array[Math.floor(Math.random() * array.length)];
  }
  function generateRandomId() {
    return Math.random().toString(36).substr(2, 9);
  }

  function generateRandomProjects(numberOfProjects) {
    const projects = [];

    const names = ["Astro", "BioTech", "Enviro", "CompSci", "Mechano"];
    const overviews = [
      "Analyzing stars",
      "Medicine research",
      "Pollution control",
      "AI development",
      "Automotive engineering",
    ];
    const skills = ["Python", "Java", "Biology", "Physics", "Mathematics"];

    for (let i = 0; i < numberOfProjects; i++) {
      const name = getRandomElement(names);
      const overview = getRandomElement(overviews);
      const skillSet = new Set();

      // Add 2-4 random skills to each project
      const numberOfSkills = Math.floor(Math.random() * 3) + 6;
      for (let j = 0; j < numberOfSkills; j++) {
        skillSet.add(getRandomElement(skills));
      }

      const photoUrl = `https://picsum.photos/seed/${generateRandomId()}/320/180`;

      projects.push({
        name,
        overview,
        skills: Array.from(skillSet),
        photoUrl,
      });
    }

    return projects;
  }

  let projects: any[] = [];
  onMount(() => {
    console.warn("Generating random projects");
    projects = generateRandomProjects(20);
  });

  

  $: console.log(projects);
</script>

<div class="container">
  {#each projects as project}
    <div class="project-container">
      <img src={project.photoUrl} alt="" />
      <div class="details">
        <h3>{project.name}</h3>
        <p>{project.overview}</p>
        <div class="skills">
          {#each project.skills as skill}
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
    </div>
  {/each}
</div>

<style>
  .container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    grid-auto-rows: 1fr;
    height: 100%;
    gap: 8px;
    padding: 12px;
  }
  .project-container {
    display: grid;
    grid-template-rows: auto 1fr;
    /* justify-content: center; */
    height: 100%;
    width: 100%;

    border-radius: 16px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.22);
    aspect-ratio: 16 / 9;
    padding: 8px;
    gap: 4px;

   


    & img {
      min-width: 100%;
      width: 100%;
      
      /* height: 100%; */
      border-radius: 8px;
      object-fit: cover;
      aspect-ratio: 16 / 9;
    }
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
  .details {
    display: flex;
    flex-direction: column;
    padding: 4px;
    gap: 4px;
    
    
  }
</style>

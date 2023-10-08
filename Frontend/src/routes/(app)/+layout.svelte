<script>
  import { arrowSvg, bellSvg } from "$lib/svgs";
  import { scrollY } from "$lib/stores";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import {
    navigateBack,
    navigateForward,
    historyStore,
  } from "$lib/stores.ts";
  import * as svgs from "$lib/svgs.js";

  $: currentPage = $page.url.pathname;
</script>

<div class="container">
  <div class="left-side">
    <div class="logo-container">
      <img src="/logo252.png" alt="" />
      <p>GitTogether</p>
    </div>
    <button
      class="nav-btn"
      class:selected={currentPage == "/home"}
      on:click={() => goto("/home")}
      ><span class="icon">{@html svgs.homeSvg}</span> Home</button
    >
    <button
      class="nav-btn"
      class:selected={currentPage == "/my-projects"}
      on:click={() => goto("/my-projects")}
      ><span class="icon">{@html svgs.folderOpenDotSvg}</span>My Projects</button
    >
    <button
      class="nav-btn"
      class:selected={currentPage == "/discover"}
      on:click={() => goto("/discover")}
      ><span class="icon">{@html svgs.compassSvg}</span>Discover</button
    >
    <button
      class="nav-btn"
      class:selected={currentPage == "/messages"}
      on:click={() => goto("/messages")}
      ><span class="icon">{@html svgs.messageCircleSvg}</span>Messages</button
    >
    <button
      class="nav-btn"
      class:selected={currentPage == "/discussions"}
      on:click={() => goto("/discussions")}
      ><span class="icon">{@html svgs.peopleSvg}</span>Discussions</button
    >
    <button
      class="nav-btn"
      class:selected={currentPage.includes("/project")}
      on:click={() => goto("/project/nasa")}
      ><span class="icon">{@html svgs.folderSvg}</span>Sample Project</button
    >
  </div>
  <div
    class="right-side"
    on:scroll={(e) => {
      scrollY.set(e.target.scrollTop);
    }}
  >
    <div class="top-bar">
      <button
        class="back"
        class:unavailable={$historyStore?.history.length == 1 ||
          $historyStore?.currentIndex == 0}
        on:click={(e) => {
          navigateBack();
        }}><span class="icon">{@html arrowSvg}</span></button
      >
      <button
        class="forward"
        class:unavailable={$historyStore?.currentIndex ==
          $historyStore?.history.length - 1}
        on:click={(e) => {
          navigateForward();
        }}><span class="icon">{@html arrowSvg}</span></button
      >
      <input type="text" class="search-input" placeholder="Search" />
      <div class="icon"><span>{@html bellSvg}</span></div>
      <div class="profile-picture">
        <img src="/pic.png" alt="" />
      </div>
    </div>
    <slot />
  </div>
</div>

<style>
  .container {
    display: flex;
    flex-direction: row;
    height: 100vh;
    width: 100%;
    overflow: hidden;
  }
  .left-side {
    display: flex;
    flex-direction: column;
    padding: 12px;
    width: 220px;
    min-width: 220px;
    gap: 4px;
    height: 100%;
    background-color: #ffffff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    z-index: 11;
  }
  button {
    border: none;
    background-color: white;
    outline: none;
  }
  .nav-btn {
    display: flex;
    padding: 0 4px;
    font-size: 18px;
    height: 40px;
    align-items: center;
    border-radius: 8px;
    color: black !important;
    transition: transform 0.1s ease-in-out;
    gap: 8px;
  }
  .nav-btn:not(.selected):hover {
    background-color: #f2f2f2;
    user-select: none;
  }
  .nav-btn:active {
    background-color: #e6e6e6;
    transform: scale(0.98);
  }
  .selected {
    background-color: #e6e6e6;
  }
  .right-side {
    display: flex;
    position: relative;
    flex-direction: column;

    height: 100%;
    width: 100%;
    overflow-x: hidden;
  }
  .top-bar {
    position: sticky;
    top: 0;
    display: flex;
    align-items: center;
    height: 60px;
    width: 100%;
    background-color: white;
    padding: 8px;
    gap: 8px;
    z-index: 10;
  }
  .search-input {
    padding: 12px;
    border-radius: 12px;
    border: none;
    outline: none;
    font-size: 18px;
    width: 100%;
    height: 100%;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  }
  .back,
  .forward {
    display: flex;
    height: 100%;
    aspect-ratio: 1;
    border-radius: 8px;
    background-color: white;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    color: rgb(75, 75, 75);
    border: none;

    transition: transform 0.1s ease-in-out, scale 0.1s ease-in-out;

    &:hover {
      cursor: pointer;
      color: black;
    }
    &:active {
      background-color: rgb(250, 250, 250);
    }
    & span:hover {
      background-color: transparent;
    }
  }
  .forward {
    transform: rotate(180deg);
  }
  .profile-picture {
    display: flex;
    height: 100%;
    aspect-ratio: 1;
    border-radius: 50%;
    transition: transform 0.1s ease-in-out;

    & img {
      height: 100%;
      border-radius: 50%;
      aspect-ratio: 1;
      object-fit: cover;
    }
  }
  .profile-picture:hover {
    cursor: pointer;
    transform: scale(1.05);
  }
  .profile-picture:active {
    transform: scale(1.03);
  }

  .icon {
    display: flex;
    height: 100%;
    align-items: center;
    justify-content: center;
    aspect-ratio: 1;
    border-radius: 50%;

    transition: background-color 0.1s ease-in-out;

    & span {
      display: flex;
      height: 100%;
      align-items: center;
      justify-content: center;
      aspect-ratio: 1;
      scale: 1.4;
      border-radius: 50%;
      transition: transform 0.1s ease-in-out;
    }
  }
  .icon:hover {
    cursor: pointer;
    background-color: rgb(232, 232, 232);
  }
  .icon:active span {
    transform: scale(0.9);
  }

  .logo-container {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px;
    border-radius: 8px;
    background-color: rgb(237, 237, 237);
    transition: transform 0.1s ease-in-out;

    & img {
      height: 40px;
      aspect-ratio: 1;
      object-fit: cover;
    }
    & p {
      font-size: 24px;
      font-weight: 600;
    }
  }
</style>

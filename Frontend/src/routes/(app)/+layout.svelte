<script>
  import { bellSvg } from "$lib/svgs";
</script>

<div class="container">
  <div class="left-side">
    <div class="nav-btn">Home</div>
    <div class="nav-btn">My Projects</div>
    <div class="nav-btn">My Groups</div>
    <div class="nav-btn">Discover</div>
    <div class="nav-btn">Messages</div>
    <div class="nav-btn">Discussions</div>
  </div>
  <div class="right-side">
    <div class="top-bar">
      <input type="text" class="search-input" placeholder="Search" />
      <div class="icon"><span>{@html bellSvg}</span></div>
      <div class="profile-picture">
        <img src="/pic.png" alt="" />
      </div>
    </div>
    <slot/>
  </div>
</div>

<style>
  .container {
    display: flex;
    flex-direction: row;
    /* align-items: center; */
    /* justify-content: center; */
    height: 100vh;
    width: 100%;
    overflow: hidden;
    /* gap: 10px; */
    /* border: 1px solid red; */
  }
  .left-side {
    display: flex;
    flex-direction: column;
    padding: 12px;
    /* align-items: center; */
    /* justify-content: center; */
    width: 200px;
    height: 100%;
    background-color: #ffffff;
    /* gap: 16px; */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    /* width: 100%; */
  }
  .nav-btn {
    display: flex;
    padding: 0 12px;
    font-size: 18px;
    height: 40px;
    align-items: center;
    border-radius: 8px;
    transition: transform 0.1s ease-in-out;
  }
  .nav-btn:hover {
    background-color: #f2f2f2;
    user-select: none;
  }
  .nav-btn:active {
    background-color: #e6e6e6;
    transform: scale(0.98);

  }
  .right-side {
    display: flex;
    flex-direction: column;
    /* align-items: center; */
    /* justify-content: center; */
    /* gap: 16px; */
    /* background-color: red; */
    height: 100%;
    width: 100%;
    overflow-x: hidden;
    /* width: 100%; */
  }
  .top-bar {
    display: flex;
    align-items: center;
    height: 80px;
    width: 100%;
    /* background-color: red; */
    padding: 12px;
    gap: 8px;
  }
  .search-input {
    padding: 12px;
    border-radius: 12px;
    border: none;
    outline: none;
    font-size: 18px;
    width: 100%;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  }
  .profile-picture {
    display: flex;
    height: 70%;
    /* width: 40px; */
    aspect-ratio: 1;
    border-radius: 50%;
    /* overflow: hidden; */
    transition: transform 0.1s ease-in-out;

    & img {
      height: 100%;
      border-radius: 50%;
      /* width: 100%; */
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
    scale: 1;
    border-radius: 50%;

    transition:  background-color 0.1s ease-in-out;
    /* border: 1px solid red; */

    & span {
      display: flex;
      height: 100%;
      align-items: center;
      justify-content: center;
      aspect-ratio: 1;
      scale: 1.4;
      border-radius: 50%;
      /* width: 100%; */
      /* overflow: hidden; */
      transition: transform 0.1s ease-in-out;
    }
    /* overflow: hidden; */
  }
  .icon:hover  {

    cursor: pointer;
    background-color: rgb(232, 232, 232);

  }
  .icon:active span {
    transform: scale(0.90);


  }
</style>

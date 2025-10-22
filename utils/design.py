SKY_DESIGN_MARKDOWN = """
<style>
  /* Sidebar: transparent background; keep gradient border on the right */
  [data-testid="stSidebar"] {
      background: transparent !important;        /* let theme/background show through */
      border-right: 3px solid transparent;       /* enable a right-side border only */
      border-image: linear-gradient(180deg,
          rgba(255, 140, 0, 1) 8%,
          rgba(248, 0, 50, 1) 27%,
          rgba(255, 0, 160, 1) 40%,
          rgba(140, 40, 255, 1) 59%,
          rgba(0, 35, 255, 1) 80%,
          rgba(25, 160, 255, 1) 96%) 1;
  }

  /* Ensure no inner layers reintroduce a background color */
  [data-testid="stSidebar"] > div:first-child,
  [data-testid="stSidebarContent"] {
      background: transparent !important;
  }

  .centered-header {
      text-align: center;
      font-size: 2em;
      font-weight: bold;
      padding: 10px;
      margin-bottom: 50px;
      shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      border-radius: 10px;
  }
</style>
"""

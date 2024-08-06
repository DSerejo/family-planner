<script lang="ts">
     import TopAppBar, { Row, Section, Title } from '@smui/top-app-bar';
     import IconButton from '@smui/icon-button';
     let prominent = false;
        let dense = false;
        let secondaryColor = false;
</script>

<div class="top-app-bar-container w-100">
    <TopAppBar
      variant="static"
      {prominent}
      {dense}
      color={secondaryColor ? 'secondary' : 'primary'}
    >
      <Row>
        <Section>
          <IconButton class="material-symbols-outlined">menu</IconButton>
          <Title>Static</Title>
        </Section>
        <Section align="end" toolbar>
          <IconButton class="material-symbols-outlined" aria-label="Download"
            >file_download</IconButton
          >
          <IconButton class="material-symbols-outlined" aria-label="Print this page"
            >print</IconButton
          >
          <IconButton class="material-symbols-outlined" aria-label="Bookmark this page"
            >bookmark</IconButton
          >
        </Section>
      </Row>
    </TopAppBar>
    <div>
        <div class="pb-4">
            <slot></slot>
        </div>
    </div>
  </div>

  <style>
    .top-app-bar-container{
        position: relative;
    }
    :global(.smui-top-app-bar--static){
        position: sticky;
        top: 0;
        z-index: 100;
    }
  </style>
<script lang="ts">
    import TextField from "@smui/textfield";
    import Button from "@smui/button";
    
</script>
<div class="flex flex-col gap-2">
    <div class="text-lg font-bold">Create a new family</div>
    <form method="post" action="/family/create">
        <TextField type="text" input$name="familyName" label="Family Name" value="" />
        <Button type="submit">Create</Button>
    </form>
</div>
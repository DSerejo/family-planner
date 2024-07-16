export const load = async (event) => {
  console.log(event.locals.requestId)
    return {
      googleSession: await event.locals.auth(),
    }
  }
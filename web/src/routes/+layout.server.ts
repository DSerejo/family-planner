export const load = async (event) => {
  
    return {
      googleSession: await event.locals.auth(),
      session: await event.locals.session()
    }
  }
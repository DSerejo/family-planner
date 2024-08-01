import { getUserWithFamilies } from '$lib/server/user/user.queries.js'
import { redirect } from '@sveltejs/kit'
import { signOut } from '$lib/server/auth/auth'
import { setToken } from '$lib/server/api/api'

export const load = async (event) => {
    const googleSession= await event.locals.auth()
    const session = await event.locals.session()
    if(session) {
      setToken(session.token)
    }
    
    return {
      googleSession,
      session
    }
  }
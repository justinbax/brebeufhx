/**
 * Api service
 */
export const Api = {
    get (path: string, data?: any) {
      return call('get', path, data)
    },
  
    post (path: string, data?: any) {
      return call('post', path, data)
    }
  }


/**
 * Fetch wrapper
 */
async function call (method: 'get' | 'post', path: string, data?: any) {
    const options: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    }
    if (data) {
      method === 'get'
        ? path += `?${new URLSearchParams(data).toString()}`
        : options['body'] = JSON.stringify(data)
    }
  
    return fetch(`${path}`, options)
      .then(response => response.json())
  }
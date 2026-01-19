import axios from 'axios'
import { createRefresh } from 'react-auth-kit'

const refreshApi = createRefresh({
    interval: 4,
    refreshApiCallback: async (
    {
        authToken,
        authTokenExpireAt,
        refreshToken,
        refreshTokenExpiresAt,
        authUserState
    }) => {
        try {
            const response = await axios.post("users/refresh", {}, {
                headers: {'Authorization': `Bearer ${refreshToken}`}}
            )
            return {
                isSuccess: true,
                newAuthToken: response.data.access,
                newAuthTokenExpireIn: 5,
                newRefreshToken: response.data.refresh,
                newRefreshTokenExpiresIn: 5
            }
        } catch(error) {
            console.error(error)
            return {
                isSuccess: false,
                newAuthToken: "<invalid token>"
            } 
        }    
    }
})

export default refreshApi
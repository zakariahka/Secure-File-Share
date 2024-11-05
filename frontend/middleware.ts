import { NextRequest, NextResponse } from 'next/server';
import axios from './src/utils/axios';

export async function middleware(req: NextRequest) {
  console.log('Middleware is running'); 
  const cookie = req.headers.get('cookie') || '';

  try {
    const response = await axios.get('user/me', {
      headers: { Cookie: cookie },
    });

    if (!response.data.authenticated) {
      
      const loginUrl = new URL('/login', req.url);
      return NextResponse.redirect(loginUrl);
    }

    return NextResponse.next();
  } catch (error) {
    console.error("Error in middleware:", error);
    const loginUrl = new URL('/login', req.url);
    return NextResponse.redirect(loginUrl);
  }
}

export const config = {
  matcher: ['/main'],
};
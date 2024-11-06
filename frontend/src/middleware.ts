import { NextResponse, NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  console.log('middlware running (test)')
  const token = request.cookies.get('token');
  
  const pathname = request.nextUrl.pathname;
  const isAuthenticated = !!token;

  const publicRoutes = ['/login', '/signup'];

  if (!isAuthenticated && !publicRoutes.includes(pathname)) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (isAuthenticated && publicRoutes.includes(pathname)) {
    return NextResponse.redirect(new URL('/main', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/main', '/login', '/signup'],
};
import { NextResponse, NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  console.log('middlware running (test)')
  const token = request.cookies.get('token');
  
  const pathname = request.nextUrl.pathname;
  const isAuthenticated = !!token;

  const protectedRoutes = ['/main'];

  if (!isAuthenticated && protectedRoutes.includes(pathname)) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  const publicRoutes = ['/login', '/signup'];
  if (isAuthenticated && publicRoutes.includes(pathname)) {
    return NextResponse.redirect(new URL('/main', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/main', '/protected-route', '/login', '/signup'],
};

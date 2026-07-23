import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // Only inject tokens for our API
  if (!req.url.includes('/api/')) {
    return next(req);
  }

  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem('auth_session');
    if (saved) {
      try {
        const session = JSON.parse(saved);
        if (session.access_token) {
          req = req.clone({
            setHeaders: {
              Authorization: `Bearer ${session.access_token}`
            }
          });
        }
      } catch (e) {}
    }
  }
  return next(req);
};

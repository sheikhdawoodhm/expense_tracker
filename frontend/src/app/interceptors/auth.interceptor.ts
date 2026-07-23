import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { throwError, BehaviorSubject } from 'rxjs';
import { catchError, switchMap, filter, take } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);

  // Only inject tokens for our API
  if (!req.url.includes('/api/')) {
    return next(req);
  }

  let token = '';
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem('auth_session');
    if (saved) {
      try {
        const session = JSON.parse(saved);
        if (session.access_token) {
          token = session.access_token;
          req = req.clone({
            setHeaders: {
              Authorization: `Bearer ${token}`
            }
          });
        }
      } catch (e) {}
    }
  }

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      // If it's a 401 and we aren't already trying to login or refresh
      if (error.status === 401 && !req.url.includes('/api/auth/login') && !req.url.includes('/api/auth/refresh')) {
        return authService.refreshToken().pipe(
          switchMap((res) => {
            req = req.clone({
              setHeaders: {
                Authorization: `Bearer ${res.access_token}`
              }
            });
            return next(req);
          }),
          catchError((refreshError) => {
            // If refresh fails, log out
            authService.logout();
            return throwError(() => refreshError);
          })
        );
      }
      return throwError(() => error);
    })
  );
};

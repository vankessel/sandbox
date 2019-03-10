use std::ops::{Add, Div, Mul, Neg, Sub};

trait Numeric<T>:
    Add<Output = T>
    + Sub<Output = T>
    + Mul<Output = T>
    + Div<Output = T>
    + Neg<Output = T>
    + Copy
    + PartialEq
    + PartialOrd
{
}
impl Numeric<f64> for f64 {}
impl Numeric<f32> for f32 {}

#[derive(Clone, Copy, PartialEq, Debug)]
struct Complex<T: Numeric<T>> {
    a: T,
    b: T,
}

type Complex32 = Complex<f32>;
type Complex64 = Complex<f64>;

impl<T> Complex<T>
where
    T: Numeric<T>,
{
    fn new(a: T, b: T) -> Self {
        Self { a: a, b: b }
    }

    fn conj(&self) -> Self {
        Self {
            a: self.a,
            b: -self.b,
        }
    }

    fn conj_inp(&mut self) -> Self {
        self.b = -self.b;
        *self
    }
}

impl<T> Add for Complex<T>
where
    T: Numeric<T>,
{
    type Output = Self;
    fn add(self, other: Self) -> Self {
        Self {
            a: self.a + other.a,
            b: self.b + other.b,
        }
    }
}
impl<T> Add<T> for Complex<T>
where
    T: Numeric<T>,
{
    type Output = Self;
    fn add(self, other: T) -> Self {
        Self {
            a: self.a + other,
            b: self.b,
        }
    }
}
impl Add<Complex64> for f64
{
    type Output = Complex64;
    fn add(self, other: Complex64) -> Complex64 {
        Complex {
            a: other.a + self,
            b: other.b,
        }
    }
}
impl Add<Complex32> for f32
{
    type Output = Complex32;
    fn add(self, other: Complex32) -> Complex32 {
        Complex {
            a: other.a + self,
            b: other.b,
        }
    }
}

impl<T: Numeric<T>> Sub for Complex<T> {
    type Output = Self;
    fn sub(self, other: Self) -> Self {
        Self {
            a: self.a - other.a,
            b: self.b - other.b,
        }
    }
}
impl<T: Numeric<T>> Sub<T> for Complex<T> {
    type Output = Self;
    fn sub(self, other: T) -> Self {
        Self {
            a: self.a - other,
            b: self.b,
        }
    }
}
impl Sub<Complex64> for f64 {
    type Output = Complex64;
    fn sub(self, other: Complex64) -> Complex64 {
        Complex {
            a: self - other.a,
            b: -other.b,
        }
    }
}
impl Sub<Complex32> for f32 {
    type Output = Complex32;
    fn sub(self, other: Complex32) -> Complex32 {
        Complex {
            a: self - other.a,
            b: -other.b,
        }
    }
}

impl<T: Numeric<T>> Mul for Complex<T> {
    type Output = Self;
    fn mul(self, other: Self) -> Self {
        let im_half = self.b * other.b;
        Self {
            a: self.a * self.a - other.a * other.a,
            b: im_half + im_half
        }
    }
}
impl<T: Numeric<T>> Mul<T> for Complex<T> {
    type Output = Self;
    fn mul(self, other: T) -> Self {
        Self {
            a: self.a * other,
            b: self.b * other
        }
    }
}
impl Mul<Complex64> for f64 {
    type Output = Complex64;
    fn mul(self, other: Complex64) -> Complex64 {
        Complex {
            a: other.a * self,
            b: other.b * self
        }
    }
}
impl Mul<Complex32> for f32 {
    type Output = Complex32;
    fn mul(self, other: Complex32) -> Complex32 {
        Complex {
            a: other.a * self,
            b: other.b * self
        }
    }
}

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    fn construct() {
        assert_eq!(Complex { a: 1.0, b: 2.0 }, Complex::new(1.0, 2.0));
    }

    #[test]
    fn duplication() {
        let z = Complex::new(1.0, 2.0);
        assert_eq!(z, z.clone());
    }

    #[test]
    fn conjugation() {
        let z = Complex::new(1.0, 2.0);
        let w = z;
        assert_eq!(z, w.conj().conj());
        let mut w = z;
        assert_eq!(z, w.conj_inp().conj_inp());
    }

    #[test]
    fn addition() {
        let z = Complex::new(1.0, 2.0);
        assert_eq!(Complex::new(2.0, 4.0), z + z);
        assert_eq!(Complex::new(2.0, 2.0), z + 1.0);
        assert_eq!(Complex::new(2.0, 2.0), 1.0 + z);
    }

    #[test]
    fn subtraction() {
        let z = Complex::new(1.0, 2.0);
        assert_eq!(Complex::new(0.0, 0.0), z - z);
        assert_eq!(Complex::new(0.0, 2.0), z - 1.0);
        assert_eq!(Complex::new(0.0, -2.0), 1.0 - z);
    }

    #[test]
    fn multiplication() {
        let z = Complex::new(1.0, 2.0);
        assert_eq!(Complex::new(-3.0, 4.0), z * z);
    }
}

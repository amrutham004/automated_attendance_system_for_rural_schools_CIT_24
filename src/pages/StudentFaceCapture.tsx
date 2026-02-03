/**
 * StudentFaceCapture.tsx - Student Face Capture Page
 * 
 * Standalone page for students to capture their face photo
 * after their attendance has been recorded.
 * 
 * Accessed via: /face-capture?roll_no=20221CIT0043
 */

import { useState, useRef, useCallback, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import Header from '@/components/attendance/Header';
import Footer from '@/components/attendance/Footer';
import Scene3D from '@/components/3d/Scene3D';
import FloatingCard from '@/components/3d/FloatingCard';
import GlassButton from '@/components/3d/GlassButton';
import { getStudentById, hasMarkedAttendanceToday, saveFaceCapture, getFaceCapture } from '@/lib/attendanceData';
import { Camera, X, RotateCcw, Check, AlertCircle, CheckCircle, User } from 'lucide-react';

type Step = 'checking' | 'capture' | 'preview' | 'success' | 'error';

const StudentFaceCapture = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const rollNo = searchParams.get('roll_no');
  
  const [step, setStep] = useState<Step>('checking');
  const [studentName, setStudentName] = useState('');
  const [error, setError] = useState('');
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Check if student can capture face
  useEffect(() => {
    if (!rollNo) {
      setError('No student ID provided');
      setStep('error');
      return;
    }

    const student = getStudentById(rollNo);
    if (!student) {
      setError('Student not found');
      setStep('error');
      return;
    }

    setStudentName(student.name);

    // Check if attendance was marked today
    if (!hasMarkedAttendanceToday(rollNo)) {
      setError('Attendance not marked for today. Please scan the QR code first.');
      setStep('error');
      return;
    }

    // Check if face already captured
    const today = new Date().toISOString().split('T')[0];
    const existingCapture = getFaceCapture(rollNo, today);
    if (existingCapture) {
      setStep('success');
      setCapturedImage(existingCapture);
      return;
    }

    // Start camera
    setStep('capture');
    startCamera();
  }, [rollNo]);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setIsStreaming(false);
  }, []);

  const startCamera = useCallback(async () => {
    try {
      // Stop any existing stream first
      stopCamera();
      
      // Enhanced iOS detection
      const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
      const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
      
      console.log('Camera detection:', { isIOS, isSafari, userAgent: navigator.userAgent });
      
      // Progressive camera constraints - start simple, then enhance
      const constraintsList = [
        // iOS Safari specific - most compatible
        {
          video: {
            facingMode: 'user',
            width: { ideal: 320, max: 640 },
            height: { ideal: 240, max: 480 }
          },
          audio: false
        },
        // Fallback - very basic
        {
          video: true,
          audio: false
        },
        // iOS with specific constraints
        {
          video: {
            facingMode: 'user'
          },
          audio: false
        }
      ];
      
      let stream = null;
      let lastError = null;
      
      // Try each constraint set until one works
      for (let i = 0; i < constraintsList.length; i++) {
        const constraints = constraintsList[i];
        console.log(`Trying camera constraint set ${i + 1}:`, constraints);
        
        try {
          // For iOS Safari, sometimes we need to request permissions first
          if (isIOS && isSafari && i === 0) {
            console.log('iOS Safari detected - requesting permissions...');
          }
          
          stream = await navigator.mediaDevices.getUserMedia(constraints);
          console.log(`Camera access successful with constraint set ${i + 1}`);
          break; // Success - exit the loop
          
        } catch (err: any) {
          console.warn(`Constraint set ${i + 1} failed:`, err.name, err.message);
          lastError = err;
          
          // If this is a permission error, don't try other constraints
          if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
            break;
          }
        }
      }
      
      if (!stream) {
        // Handle the final error
        if (lastError) {
          console.error('All camera attempts failed:', lastError);
          
          if (lastError.name === 'NotAllowedError' || lastError.name === 'PermissionDeniedError') {
            if (isIOS) {
              setError(`Camera permission denied on iOS. 

To fix this:
1. Go to Settings > Safari > Camera
2. Set to "Allow" or "Ask"
3. Close this tab and reopen
4. Try again`);
            } else {
              setError('Camera permission denied. Please allow camera access in your browser settings.');
            }
          } else if (lastError.name === 'NotFoundError') {
            setError('No camera found. Please ensure your device has a working camera.');
          } else if (lastError.name === 'NotReadableError' || lastError.name === 'TrackStartError') {
            setError('Camera is already in use by another application. Please close other apps and try again.');
          } else if (lastError.name === 'OverconstrainedError') {
            setError('Camera does not support the required settings. Trying basic mode...');
            // Try one more time with very basic settings
            try {
              stream = await navigator.mediaDevices.getUserMedia({ video: true });
            } catch (finalErr: any) {
              setError(`Camera access failed: ${finalErr.message}`);
            }
          } else {
            setError(`Camera access failed: ${lastError.message}. Please try refreshing the page.`);
          }
        } else {
          setError('Unknown camera error occurred. Please try refreshing the page.');
        }
        return;
      }
      
      // Success - set up the stream
      streamRef.current = stream;
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        
        // Wait for video to be ready
        videoRef.current.onloadedmetadata = () => {
          // iOS Safari specific handling
          if (isIOS && isSafari) {
            console.log('iOS Safari video loaded - ensuring playback...');
            // Add a small delay for iOS
            setTimeout(() => {
              videoRef.current?.play().catch(playErr => {
                console.error('iOS video play failed:', playErr);
                setError('Video playback failed on iOS. Please try again.');
              });
            }, 100);
          } else {
            videoRef.current?.play().catch(playErr => {
              console.error('Video play failed:', playErr);
            });
          }
          
          // Add a small delay before setting streaming state
          setTimeout(() => {
            setIsStreaming(true);
            setError(null);
          }, 200);
        };
        
        // Handle video errors
        videoRef.current.onerror = (videoErr) => {
          console.error('Video element error:', videoErr);
          setError('Video display error. Please try again.');
        };
      }
      
    } catch (err: any) {
      console.error('Camera initialization failed:', err);
      setError(`Failed to start camera: ${err.message || 'Unknown error'}`);
    }
  }, [stopCamera]);

  const capturePhoto = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    
    if (!context) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    setCapturedImage(imageData);
    setStep('preview');
    stopCamera();
  }, [stopCamera]);

  const retakePhoto = useCallback(() => {
    setCapturedImage(null);
    setStep('capture');
    startCamera();
  }, [startCamera]);

  const confirmCapture = useCallback(() => {
    if (!capturedImage || !rollNo) return;
    
    const today = new Date().toISOString().split('T')[0];
    saveFaceCapture(rollNo, today, capturedImage);
    setStep('success');
  }, [capturedImage, rollNo]);

  // Cleanup camera on unmount
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, [stopCamera]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white overflow-hidden">
      <Scene3D />
      <Header />

      <main className="container relative z-10 py-8 max-w-lg">
        {/* Page Header */}
        <div className="text-center mb-6">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-teal-500/20 border border-cyan-500/30 flex items-center justify-center">
            <Camera size={32} className="text-cyan-400" />
          </div>
          <h1 className="text-2xl font-bold font-display bg-gradient-to-r from-cyan-300 to-teal-300 bg-clip-text text-transparent mb-2">
            Face Verification
          </h1>
          {studentName && (
            <p className="text-cyan-100/70">
              {rollNo} – {studentName}
            </p>
          )}
        </div>

        {/* Checking State */}
        {step === 'checking' && (
          <FloatingCard>
            <div className="text-center py-8">
              <div className="animate-pulse text-cyan-400 font-medium">
                Checking eligibility...
              </div>
            </div>
          </FloatingCard>
        )}

        {/* Capture State */}
        {step === 'capture' && (
          <div className="space-y-6 animate-fade-in">
            <FloatingCard>
              <div className="space-y-4">
                {/* Camera View */}
                <div className="aspect-[4/3] bg-black rounded-xl overflow-hidden relative">
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-full object-cover"
                  />
                  
                  {/* Face guide overlay */}
                  {isStreaming && (
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                      <div className="w-40 h-48 border-2 border-cyan-400/50 rounded-full shadow-lg shadow-cyan-500/20" />
                    </div>
                  )}
                </div>

                {error && (
                  <div className="space-y-3">
                    <p className="text-sm text-red-400 text-center">{error}</p>
                    
                    {/* Retry Camera Button */}
                    <GlassButton 
                      onClick={startCamera} 
                      className="w-full"
                      variant="secondary"
                    >
                      <Camera size={18} />
                      Retry Camera Access
                    </GlassButton>
                  </div>
                )}

                {/* Capture Button */}
                {!error && (
                  <GlassButton 
                    onClick={capturePhoto} 
                    disabled={!isStreaming}
                    className="w-full"
                    variant="primary"
                  >
                    <Camera size={18} />
                    Capture Face
                  </GlassButton>
                )}
              </div>
            </FloatingCard>

            {/* Instructions */}
            <FloatingCard glowColor="rgba(168, 85, 247, 0.2)">
              <div className="flex items-start gap-3">
                <User size={20} className="text-purple-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium text-sm text-white">Position Your Face</p>
                  <p className="text-sm text-purple-100/70 mt-1">
                    Center your face within the oval guide and ensure good lighting.
                  </p>
                </div>
              </div>
            </FloatingCard>
          </div>
        )}

        {/* Preview State */}
        {step === 'preview' && capturedImage && (
          <div className="space-y-6 animate-fade-in">
            <FloatingCard>
              <div className="space-y-4">
                {/* Captured Image */}
                <div className="aspect-[4/3] rounded-xl overflow-hidden">
                  <img
                    src={capturedImage}
                    alt="Captured face"
                    className="w-full h-full object-cover"
                  />
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3">
                  <GlassButton
                    variant="secondary"
                    onClick={retakePhoto}
                    className="flex-1"
                  >
                    <RotateCcw size={18} />
                    Retake
                  </GlassButton>
                  
                  <GlassButton
                    variant="primary"
                    onClick={confirmCapture}
                    className="flex-1"
                  >
                    <Check size={18} />
                    Confirm
                  </GlassButton>
                </div>
              </div>
            </FloatingCard>
          </div>
        )}

        {/* Success State */}
        {step === 'success' && (
          <div className="animate-scale-in">
            <FloatingCard glowColor="rgba(34, 197, 94, 0.3)">
              <div className="text-center space-y-4 py-4">
                <div className="w-20 h-20 mx-auto rounded-full bg-green-500/20 flex items-center justify-center">
                  <CheckCircle size={40} className="text-green-400" />
                </div>
                
                <h2 className="text-xl font-bold font-display text-green-400">
                  Verification Complete!
                </h2>
                
                <p className="text-cyan-100/70">
                  Your attendance and face photo have been recorded successfully.
                </p>

                {capturedImage && (
                  <div className="w-32 h-32 mx-auto rounded-full overflow-hidden border-4 border-green-500/30">
                    <img
                      src={capturedImage}
                      alt="Your face"
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}

                <div className="pt-4">
                  <GlassButton to="/" variant="secondary" className="w-full">
                    Return to Home
                  </GlassButton>
                </div>
              </div>
            </FloatingCard>
          </div>
        )}

        {/* Error State */}
        {step === 'error' && (
          <div className="animate-scale-in">
            <FloatingCard glowColor="rgba(239, 68, 68, 0.3)">
              <div className="text-center space-y-4 py-4">
                <div className="w-20 h-20 mx-auto rounded-full bg-red-500/20 flex items-center justify-center">
                  <AlertCircle size={40} className="text-red-400" />
                </div>
                
                <h2 className="text-xl font-bold font-display text-red-400">
                  Cannot Capture Face
                </h2>
                
                <p className="text-cyan-100/70">{error}</p>

                <div className="pt-4">
                  <GlassButton to="/" variant="secondary" className="w-full">
                    Return to Home
                  </GlassButton>
                </div>
              </div>
            </FloatingCard>
          </div>
        )}

        {/* Hidden canvas for capture */}
        <canvas ref={canvasRef} className="hidden" />
      </main>

      <Footer />
    </div>
  );
};

export default StudentFaceCapture;

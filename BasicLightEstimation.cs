using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.XR.ARFoundation;
using System;
using System.Collections;
using System.Diagnostics;
using System.IO;
using UnityEngine.Networking;
using Siccity.GLTFUtility;

namespace UnityEngine.XR.ARFoundation.Samples
{
    /// <summary>
    /// A component that can be used to access the most recently received basic light estimation information
    /// for the physical environment as observed by an AR device.
    /// </summary>
    [RequireComponent(typeof(Light))]
    public class BasicLightEstimation : MonoBehaviour
    {
        [SerializeField]
        [Tooltip("The ARCameraManager which will produce frame events containing light estimation information.")]
        ARCameraManager m_CameraManager;

        /// <summary>
        /// Get or set the <c>ARCameraManager</c>.
        /// </summary>
        public ARCameraManager cameraManager
        {
            get { return m_CameraManager; }
            set
            {
                if (m_CameraManager == value)
                    return;

                if (m_CameraManager != null)
                    m_CameraManager.frameReceived -= FrameChanged;

                m_CameraManager = value;

                if (m_CameraManager != null & enabled)
                    m_CameraManager.frameReceived += FrameChanged;
            }
        }

        /// <summary>
        /// The estimated brightness of the physical environment, if available.
        /// </summary>
        public float? brightness { get; private set; }

        /// <summary>
        /// The estimated color temperature of the physical environment, if available.
        /// </summary>
        public float? colorTemperature { get; private set; }

        /// <summary>
        /// The estimated color correction value of the physical environment, if available.
        /// </summary>
        public Color? colorCorrection { get; private set; }

        //camera
        public GameObject _camera;

        //holograms downloaded from edge
        public GameObject _light;
        public GameObject _dark;
        private string modelRequested;
        public string downloadStatus = "Initializing";
        private bool lightRequested = false;
        private bool darkRequested = false;

        //network settings
        public string edge = "http://192.168.0.6:8000/";
        private string edgeLight;
        private string edgeDark;

        //model storage location
        string filePath;

        //timestamp for results file name
        private string session_timestamp;

        //timing
        private string latency;
        private Stopwatch stopWatch = new Stopwatch();

        //output results
        private string resultsPath;

        void Awake ()
        {
            m_Light = GetComponent<Light>();
        }

        private void Start()
        {
            edgeLight = edge + "fish.glb";
            edgeDark = edge + "jellyfish.glb";
            filePath = $"{Application.persistentDataPath}/Files/";

            session_timestamp = DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss");
            resultsPath = Application.persistentDataPath + "/downloads_" + session_timestamp + ".txt";

            _light.SetActive(false);
            _dark.SetActive(false);
        }

        void OnEnable()
        {
            if (m_CameraManager != null)
                m_CameraManager.frameReceived += FrameChanged;
        }

        void OnDisable()
        {
            if (m_CameraManager != null)
                m_CameraManager.frameReceived -= FrameChanged;
        }

        void Update()
        {
            _light.transform.position = _camera.transform.position + _camera.transform.forward * 2.0f;
            _dark.transform.position = _camera.transform.position + _camera.transform.forward * 2.0f;
        }

        void FrameChanged(ARCameraFrameEventArgs args)
        {
            if (args.lightEstimation.averageBrightness.HasValue)
            {
                brightness = args.lightEstimation.averageBrightness.Value;
                m_Light.intensity = brightness.Value;
                if (brightness.Value > 0.2f)
                {
                    if (lightRequested == false)
                    {
                        modelRequested = "light";
                        DownloadFile(edgeLight);
                        lightRequested = true;
                    }
                    _light.SetActive(true);
                    _dark.SetActive(false);
                }
                else if (brightness.Value < 0.2f)
                {
                    if (darkRequested == false)
                    {
                        modelRequested = "dark";
                        DownloadFile(edgeDark);
                        darkRequested = true;
                    }
                    _dark.SetActive(true);
                    _light.SetActive(false);
                }
            }
            else
            {
                brightness = null;
            }

            if (args.lightEstimation.averageColorTemperature.HasValue)
            {
                colorTemperature = args.lightEstimation.averageColorTemperature.Value;
                m_Light.colorTemperature = colorTemperature.Value;
            }
            else
            {
                colorTemperature = null;
            }

            if (args.lightEstimation.colorCorrection.HasValue)
            {
                colorCorrection = args.lightEstimation.colorCorrection.Value;
                m_Light.color = colorCorrection.Value;
            }
            else
            {
                colorCorrection = null;
            }
        }

        public void DownloadFile(string url)
        {
            //Start timing
            stopWatch.Start();

            string path = GetFilePath(url);

            downloadStatus = "Downloading " + modelRequested + " model...";

            StartCoroutine(GetFileRequest(url, (UnityWebRequest req) =>
            {
                if (req.result == UnityWebRequest.Result.ConnectionError)
                {
                    downloadStatus = "Network error";
                }
                else if (req.result == UnityWebRequest.Result.ProtocolError)
                {
                    downloadStatus = "HTTP error";
                }
                else
                {
                    //Start the import process
                    ImportGLBAsync(path);
                }
            }));
        }

        string GetFilePath(string url)
        {
            string[] pieces = url.Split('/');
            string filename = pieces[pieces.Length - 1];

            return $"{filePath}{filename}";
        }

        void ImportGLBAsync(string filepath)
        {
            Importer.ImportGLBAsync(filepath, new ImportSettings(), OnFinishAsync, OnProgressAsync);
        }

        private void OnProgressAsync(float obj)
        {
            
        }

        private void OnFinishAsync(GameObject model, AnimationClip[] animation)
        {
            downloadStatus = "Finished downloading " + modelRequested + " model";
            latency = stopWatch.Elapsed.ToString();
            stopWatch.Reset();

            //display downloaded model in front of the camera
            if (modelRequested == "light")
            {
                _light = model;
                _light.transform.localScale = new Vector3(0.05f, 0.05f, 0.05f);
                _light.transform.Rotate(0.0f, -90.0f, 0.0f, Space.World);
            }
            else if (modelRequested == "dark")
            {
                _dark = model;
                _dark.transform.localScale = new Vector3(0.05f, 0.05f, 0.05f);
                _dark.transform.Rotate(0.0f, 0.0f, 90.0f, Space.World);
            }

            //append download latency to network traffic output file
            using (StreamWriter sw = File.AppendText(resultsPath))
            {
                sw.WriteLine(modelRequested + ": " + latency);
            }
        }

        IEnumerator GetFileRequest(string url, Action<UnityWebRequest> callback)
        {
            using (UnityWebRequest req = UnityWebRequest.Get(url))
            {
                req.downloadHandler = new DownloadHandlerFile(GetFilePath(url));
                yield return req.SendWebRequest();
                callback(req);
            }
        }

        Light m_Light;
    }
}

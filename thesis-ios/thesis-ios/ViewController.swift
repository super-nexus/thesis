//
//  ViewController.swift
//  thesis-ios
//
//  Created by Andrija Kuzmanov on 6/27/21.
//

import UIKit

class ViewController: UIViewController {
    
    @IBOutlet weak var usernameInput: UITextField!
    @IBOutlet weak var passwordInput: UITextField!
    @IBOutlet weak var loginButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    
    @IBAction func loginButtonOnClick(_ sender: Any) {
        
        let parameters = ["username" : usernameInput.text, "password": passwordInput.text]
        let url = URL(string: "https://andrija-thesis.herokuapp.com/login")!
        let session = URLSession.shared
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        do{
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted)
        } catch let error{
            print(error.localizedDescription)
        }
        
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let task = session.dataTask(with: request as URLRequest, completionHandler:{ data, response, error in
            
            guard error == nil else {
                return
            }

            guard let data = data else {
                return
            }
            
            let message = String(decoding: data, as: UTF8.self)
            
            if message == "OK"{
                DispatchQueue.main.async {
                    let storyboard = UIStoryboard(name: "Main", bundle: nil);
                    let vc = storyboard.instantiateViewController(withIdentifier: "SecondPage");
                    self.present(vc, animated: true, completion: nil);
                }
            }
            
        })
        
        task.resume()
        
    }
    
}


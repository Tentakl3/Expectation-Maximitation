import math

class Exp_Max:
    def __init__(self, documents, vocabulary):
        self.documents = documents
        self.vocabulary = vocabulary
        self.theta_d = 0.5
        self.theta_B = 0.5

    def main(self):
        d_vocabulary = self.document_vocabulary(123)
        cwd = self.c_w_d(d_vocabulary, 123)
        pw_theta_d = self.p_w_theta(d_vocabulary)
        pw_theta_B= self.p_w_theta_B(d_vocabulary, 123)

        for i in range(100):
            pzl = self.p_z_l(d_vocabulary, pw_theta_d, pw_theta_B)
            pw_theta_d = self.p_w_theta_d(d_vocabulary, pzl, cwd)
            self.update_theta(d_vocabulary, pzl, cwd)
            ll = self.log_likelihood(d_vocabulary, cwd, pw_theta_d, pw_theta_B)
            print(f"Iteración {i}: log-verosimilitud = {ll}")
            if i > 0 and abs(ll - prev_ll) < 1e-6:
                break
            prev_ll = ll
            print(pzl)

    def document_vocabulary(self, n_document):
        document_vocabulary = []
        for tok in self.documents[n_document]:
            if tok not in document_vocabulary:
                document_vocabulary.append(tok)
        
        return document_vocabulary

    def c_w_d(self, document_vocabulary, n_document):
        count = {}
        for v in document_vocabulary:
            count[v] = self.documents[n_document].count(v)

        return count

    def p_w_theta(self, document_vocabulary):
        frequency = {}
        for v in document_vocabulary:
            frequency[v] = 1/len(document_vocabulary)

        return frequency

    def p_z_l(self, document_vocabulary, pw_theta, pw_theta_B):
        e = {}
        for v in document_vocabulary:
            e[v] = (self.theta_d * pw_theta[v])/(self.theta_d * pw_theta[v] + self.theta_B * pw_theta_B[v])

        return e

    def p_w_theta_B(self, document_vocabulary, n_document):
        frequency = {}
        for v in document_vocabulary:
            frequency[v] = self.documents[n_document].count(v)/len(self.documents[n_document])

        return frequency
    
    def p_w_theta_d(self, document_vocabulary, p_z_l, c_w_d):
        count = 0
        for v in document_vocabulary:
            count = count + c_w_d[v]*p_z_l[v]

        res = {}
        for v in document_vocabulary:
            res[v] = (c_w_d[v] * p_z_l[v])/count

        return res

    def log_likelihood(self, document_vocabulary, c_w_d, pw_theta_d, pw_theta_B):
        log_likelihood = 0
        for v in document_vocabulary:
            prob = (self.theta_d * pw_theta_d[v]) + (self.theta_B * pw_theta_B[v])
            if prob > 0:
                log_likelihood += c_w_d[v] * math.log(prob)

        return log_likelihood
    
    def update_theta(self, document_vocabulary, p_z_l, c_w_d):
        total_weight = sum(c_w_d[v] for v in document_vocabulary)
        theta_d_new = sum(c_w_d[v] * p_z_l[v] for v in document_vocabulary) / total_weight
        self.theta_d = theta_d_new
        self.theta_B = 1 - self.theta_d